provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.launchflow_project
      Environment = var.launchflow_environment
    }
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

data "aws_subnets" "lf_vpc_subnets" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  tags = {
    "Project" : var.launchflow_project,
    "Environment" : var.launchflow_environment
    "Public" : "true"
  }
}

resource "aws_security_group" "docker_sg" {
  name        = "${var.launchflow_project}-${var.launchflow_environment}-${var.resource_name}-docker-sg"
  description = "Allow inbound traffic"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.firewall_cfg.expose_ports

    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  # ssh access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

locals {
  sorted_subnets = sort(data.aws_subnets.lf_vpc_subnets.ids)
}


resource "tls_private_key" "rsa_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "${var.launchflow_project}-${var.launchflow_environment}-${var.resource_name}-key"
  public_key = tls_private_key.rsa_key.public_key_openssh
}


resource "aws_instance" "docker_host" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  subnet_id     = local.sorted_subnets[0]
  key_name      = aws_key_pair.generated_key.key_name

  root_block_device {
    volume_size = var.disk_size_gb
  }

  user_data = <<EOF
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
ENV_VAR_FLAGS="${join(" ", [for k, v in var.docker_cfg.environment_variables : format("-e %s=%s", k, v)])}"
PORTS="${join(" ", [for port in var.firewall_cfg.expose_ports : format("-p %s:%s", port, port)])}"
docker run --name ${var.resource_name} -d $${PORTS} $${ENV_VAR_FLAGS} ${var.docker_cfg.image} ${join(" ", var.docker_cfg.args)}
EOF

  vpc_security_group_ids = [
    aws_security_group.docker_sg.id
  ]

  tags = {
    Project     = var.launchflow_project
    Environment = var.launchflow_environment
    Name        = "${var.resource_name}-${var.launchflow_environment}"
  }

  monitoring              = true
  disable_api_termination = false
  ebs_optimized           = true
}

locals {
  vm_ip = aws_instance.docker_host.public_ip

  connection_bucket_contents = merge({
    private_key = tls_private_key.rsa_key.private_key_pem,
    vm_ip       = local.vm_ip,
    ports       = var.firewall_cfg.expose_ports,
  }, var.additional_outputs)
}


resource "aws_s3_object" "connection_info" {
  bucket     = var.artifact_bucket
  key        = "resources/${var.resource_name}.yaml"
  depends_on = [aws_instance.docker_host]
  override_provider {
    default_tags {
      tags = {}
    }
  }
  content = <<EOF
${yamlencode(local.connection_bucket_contents)}
EOF
}

output "private_key" {
  value     = tls_private_key.rsa_key.private_key_pem
  sensitive = true
}

output "vm_ip" {
  value = local.vm_ip
}

output "ports" {
  value = yamlencode(var.firewall_cfg.expose_ports)
}

output "additional_outputs" {
  value = var.additional_outputs
}

output "aws_arn" {
  value = aws_instance.docker_host.arn
}
