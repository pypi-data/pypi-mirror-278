provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# TODO: Replace this with a memorystore resource block instead of using the module
module "memorystore_redis" {
  source                  = "terraform-google-modules/memorystore/google"
  version                 = "~> 8.0"
  name                    = var.resource_name
  project                 = var.gcp_project_id
  region                  = var.gcp_region
  enable_apis             = true
  tier                    = var.redis_tier
  memory_size_gb          = var.memory_size_gb
  auth_enabled            = true
  transit_encryption_mode = "SERVER_AUTHENTICATION"
}


resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
host: "${module.memorystore_redis.host}"
port: "${module.memorystore_redis.port}"
password: "${module.memorystore_redis.auth_string}"
EOF
}


output "host" {
  description = "The IP address of the instance."
  value       = module.memorystore_redis.host
}

output "port" {
  description = "The port number of the exposed Redis endpoint."
  value       = module.memorystore_redis.port
}

output "password" {
  description = "AUTH String set on the instance. This field will only be populated if auth_enabled is true."
  value       = module.memorystore_redis.auth_string
  sensitive   = true
}

output "gcp_id" {
  value = module.memorystore_redis.id
}
