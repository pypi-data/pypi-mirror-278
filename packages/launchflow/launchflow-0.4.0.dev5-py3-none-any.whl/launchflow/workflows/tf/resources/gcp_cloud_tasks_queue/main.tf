provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_cloud_tasks_queue_iam_member" "cloud_tasks_iam" {
  name   = google_cloud_tasks_queue.queue.name
  role   = "roles/cloudtasks.admin"
  member = "serviceAccount:${var.environment_service_account_email}"
}

resource "google_cloud_tasks_queue" "queue" {
  name       = var.resource_name
  location   = var.location == null ? var.gcp_region : var.location
  depends_on = [google_project_service.cloud_tasks]
}

resource "google_project_service" "cloud_tasks" {
  project            = var.gcp_project_id
  service            = "cloudtasks.googleapis.com"
  disable_on_destroy = false

}

resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
queue_id: "${google_cloud_tasks_queue.queue.id}"
EOF
}


output "queue_id" {
  value = google_cloud_tasks_queue.queue.id
}

output "gcp_id" {
  value = google_cloud_tasks_queue.queue.id
}
