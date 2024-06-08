#
# Launchflow global variables
#
variable "aws_region" {
  type = string
}

variable "resource_name" {
  type = string
}

variable "artifact_bucket" {
  type = string
}

variable "launchflow_project" {
  type = string
}

variable "launchflow_environment" {
  type = string
}

variable "env_role_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

#
# Secret specific variables
#
variable "recovery_window_in_days" {
  type    = number
  default = 30
}
