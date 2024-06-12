provider "aws" {
  region = var.aws_region
}

resource "aws_secretsmanager_secret" "secret" {
  name                    = var.resource_name
  recovery_window_in_days = var.recovery_window_in_days
  tags = {
    "Project" : var.launchflow_project,
    "Environment" : var.launchflow_environment
  }
}


resource "aws_s3_object" "connection_info" {
  bucket  = var.artifact_bucket
  key     = "resources/${var.resource_name}.yaml"
  content = <<EOF
secret_id: "${aws_secretsmanager_secret.secret.id}"
EOF
}


output "aws_arn" {
  value = aws_secretsmanager_secret.secret.arn
}
