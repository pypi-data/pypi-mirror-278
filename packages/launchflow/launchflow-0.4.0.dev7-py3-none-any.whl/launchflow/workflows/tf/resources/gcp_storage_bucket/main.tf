provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket_iam_member" "bucket_iam" {
  bucket = google_storage_bucket.bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.environment_service_account_email}"
}

resource "google_storage_bucket" "bucket" {
  name          = var.resource_name
  project       = var.gcp_project_id
  location      = var.location
  force_destroy = var.force_destroy
}

resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
bucket_name: "${google_storage_bucket.bucket.name}"
EOF
}


output "bucket_name" {
  value = google_storage_bucket.bucket.name
}

output "url" {
  value = google_storage_bucket.bucket.url
}

output "gcp_id" {
  value = google_storage_bucket.bucket.id
}
