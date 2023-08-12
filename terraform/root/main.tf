terraform {
  backend "gcs" {
    bucket = "hack-space-dev-terraform"
    prefix = "github.com/antoinedao/funckle/terraform/root"
  }
}

provider "google" {
  project = local.gcp-project
  region  = local.gcp-region
  zone    = local.gcp-zone
}
