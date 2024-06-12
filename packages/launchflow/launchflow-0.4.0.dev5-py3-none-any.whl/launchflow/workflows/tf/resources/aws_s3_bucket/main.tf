provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.resource_name
  tags = {
    "Project" : var.launchflow_project,
    "Environment" : var.launchflow_environment
  }
  force_destroy = var.force_destroy
}

resource "aws_iam_policy" "policy" {
  name = "${var.launchflow_project}-${var.launchflow_environment}-${var.resource_name}-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:*",
        ]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.s3_bucket.arn}",
          "${aws_s3_bucket.s3_bucket.arn}/*"
        ]
      },
    ]
  })
  tags = {
    "Project" : var.launchflow_project,
    "Environment" : var.launchflow_environment
  }
}

resource "aws_iam_role_policy_attachment" "policy_attach" {
  role       = var.env_role_name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_s3_object" "connection_info" {
  bucket     = var.artifact_bucket
  depends_on = [aws_iam_policy.policy]
  key        = "resources/${var.resource_name}.yaml"
  content    = <<EOF
bucket_name: "${aws_s3_bucket.s3_bucket.bucket}"
EOF
}


output "bucket_name" {
  value = aws_s3_bucket.s3_bucket.bucket
}

output "aws_arn" {
  value = aws_s3_bucket.s3_bucket.arn
}
