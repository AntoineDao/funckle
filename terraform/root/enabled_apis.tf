resource "google_project_service" "service" {
  project = local.gcp-project
  service = "artifactregistry.googleapis.com"

  disable_on_destroy = false
}
