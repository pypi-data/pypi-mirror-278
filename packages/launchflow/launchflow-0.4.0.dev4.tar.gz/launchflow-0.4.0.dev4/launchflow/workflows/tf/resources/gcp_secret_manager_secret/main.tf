provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_secret_manager_secret_iam_member" "secret_iam" {
  secret_id = google_secret_manager_secret.secret.secret_id
  role      = "roles/secretmanager.admin"
  member    = "serviceAccount:${var.environment_service_account_email}"
}

resource "google_secret_manager_secret" "secret" {
  secret_id = var.resource_name
  project   = var.gcp_project_id
  replication {
    auto {}
  }
}

output "secret_name" {
  value = google_secret_manager_secret.secret.name
}

output "gcp_id" {
  value = google_secret_manager_secret.secret.id
}


resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
secret_name: "${google_secret_manager_secret.secret.name}"
EOF
}
