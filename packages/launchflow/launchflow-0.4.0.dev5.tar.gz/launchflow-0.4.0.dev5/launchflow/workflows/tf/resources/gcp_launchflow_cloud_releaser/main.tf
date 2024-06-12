provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

locals {
  release_roles = [
    # Allow triggering cloud build in the project
    "roles/cloudbuild.builds.editor",
    # Allow pushing to the artifact registry
    "roles/artifactregistry.writer",
    # Allow deploying to cloud run
    "roles/run.admin",
    # TODO: add additional roles / make this configurable in the future
  ]
}

resource "google_service_account" "launchflow_releaser" {
  account_id   = var.resource_name
  display_name = "LaunchFlow Release Service Account"
  description  = "Service account that is used by LaunchFlow to trigger deployments and promotions."
}

resource "google_service_account_iam_member" "launchflow_service_account_user" {
  service_account_id = google_service_account.launchflow_releaser.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.launchflow_service_account}"
}

resource "google_storage_bucket_iam_member" "bucket_iam" {
  bucket = var.artifact_bucket
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.launchflow_releaser.email}"
}

resource "google_project_iam_member" "cloud_run_releaser" {
  count   = length(local.release_roles)
  project = var.gcp_project_id
  role    = local.release_roles[count.index]
  member  = "serviceAccount:${google_service_account.launchflow_releaser.email}"
}

output "gcp_id" {
  value = google_service_account.launchflow_releaser.id
}

resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
service_account_email: "${google_service_account.launchflow_releaser.email}"
EOF
}
