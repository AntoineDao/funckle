locals {
  gcp-project = "hack-space-dev"
  gcp-region  = "europe-west2"
  gcp-zone    = "europe-west2-a"
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "funckle"
}

data "google_project" "project" {
  project_id = local.gcp-project
}
