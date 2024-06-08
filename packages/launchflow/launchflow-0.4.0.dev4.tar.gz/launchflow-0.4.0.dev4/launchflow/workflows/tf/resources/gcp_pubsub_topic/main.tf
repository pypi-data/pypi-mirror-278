provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_pubsub_topic_iam_member" "topic_iam" {
  topic  = google_pubsub_topic.topic.name
  role   = "roles/pubsub.admin"
  member = "serviceAccount:${var.environment_service_account_email}"
}


resource "google_pubsub_topic" "topic" {
  name                       = var.resource_name
  message_retention_duration = var.message_retention_duration
}

resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
topic_id: "${google_pubsub_topic.topic.id}"
EOF
}


output "topic_id" {
  value = google_pubsub_topic.topic.id
}

output "gcp_id" {
  value = google_pubsub_topic.topic.id
}
