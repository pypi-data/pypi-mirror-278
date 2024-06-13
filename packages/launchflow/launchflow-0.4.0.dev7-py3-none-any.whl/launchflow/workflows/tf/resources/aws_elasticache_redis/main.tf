provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.launchflow_project
      Environment = var.launchflow_environment
    }
  }
}

resource "random_password" "user-password" {
  length  = 16
  special = false
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

resource "aws_elasticache_subnet_group" "default" {
  name       = "${var.launchflow_project}-${var.launchflow_environment}-${var.resource_name}-subnet-group"
  subnet_ids = toset(data.aws_subnets.lf_vpc_subnets.ids)
}

# Define a Security Group for public access (only for public instances)
resource "aws_security_group" "redis_sg" {
  name        = "${var.launchflow_project}-${var.launchflow_environment}-${var.resource_name}-redis-sg"
  description = "Allow inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project     = var.launchflow_project
    Environment = var.launchflow_environment
  }
}


resource "aws_elasticache_replication_group" "default" {
  num_cache_clusters = 1
  # NOTE: num_cache_clusters must be set to 2+ to enable failover
  automatic_failover_enabled = false

  apply_immediately    = true
  replication_group_id = "${var.resource_name}-group"
  description          = "Redis Replication Group managed by Launchflow"
  node_type            = var.node_type
  parameter_group_name = var.parameter_group_name
  engine_version       = var.engine_version
  port                 = 6379
  security_group_ids   = toset([aws_security_group.redis_sg.id])

  subnet_group_name = aws_elasticache_subnet_group.default.name

  transit_encryption_enabled = true
  auth_token                 = random_password.user-password.result
  auth_token_update_strategy = "ROTATE"

  lifecycle {
    ignore_changes = [num_cache_clusters]
  }

  tags = {
    Project     = var.launchflow_project
    Environment = var.launchflow_environment
  }
}


resource "aws_s3_object" "connection_info" {
  bucket     = var.artifact_bucket
  key        = "resources/${var.resource_name}.yaml"
  depends_on = [aws_elasticache_replication_group.default]
  override_provider {
    default_tags {
      tags = {}
    }
  }
  content = <<EOF
host: "${aws_elasticache_replication_group.default.primary_endpoint_address}"
port: 6379
password: "${random_password.user-password.result}"
EOF
}


output "host" {
  value = aws_elasticache_replication_group.default.primary_endpoint_address
}

output "port" {
  value = 6379
}

output "password" {
  value     = random_password.user-password.result
  sensitive = true
}

output "aws_arn" {
  value = aws_elasticache_replication_group.default.arn
}
