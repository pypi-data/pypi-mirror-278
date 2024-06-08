provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

locals {
  vm_ip = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip

  connection_bucket_contents = merge({
    vm_ip = local.vm_ip,
    ports = var.firewall_cfg.expose_ports,
  }, var.additional_outputs)
}

resource "random_uuid" "firewall_tag_uuid" {}


resource "google_compute_instance" "vm" {
  name         = format("%s-%s", var.resource_name, substr(md5(var.docker_cfg.image), 0, 8))
  machine_type = var.machine_type
  zone         = "${var.gcp_region}-a"

  boot_disk {
    initialize_params {
      image = "cos-cloud/cos-stable-109-17800-147-54"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
    gce-container-declaration = yamlencode({
      spec = {
        containers    = [{ image = var.docker_cfg.image, env = var.docker_cfg.environment_variables, volumeMounts = [], args = var.docker_cfg.args }]
        volumes       = []
        restartPolicy = "Always"
      }
    })
  }

  labels = {
    container-vm = "cos-stable-109-17800-147-54"
  }

  service_account {
    email  = var.environment_service_account_email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  tags = length(var.firewall_cfg.expose_ports) > 0 ? ["vm-${random_uuid.firewall_tag_uuid.result}"] : []
}

resource "google_compute_firewall" "vm_firewall" {
  # Disable setting up the firewall if no ports are configured to be exposed
  count = length(var.firewall_cfg.expose_ports) > 0 ? 1 : 0

  name    = "allow-vm-${random_uuid.firewall_tag_uuid.result}"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = var.firewall_cfg.expose_ports
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["vm-${random_uuid.firewall_tag_uuid.result}"]
}

resource "google_storage_bucket_object" "connection_info" {
  bucket  = var.artifact_bucket
  name    = "resources/${var.resource_name}.yaml"
  content = <<EOF
${yamlencode(local.connection_bucket_contents)}
EOF
}


output "vm_ip" {
  value = local.vm_ip
}

output "ports" {
  value = yamlencode(var.firewall_cfg.expose_ports)
}

# TODO try to dynamically flatten outputs
output "additional_outputs" {
  value = var.additional_outputs
}

output "gcp_id" {
  value = google_compute_instance.vm.id
}
