
resource "google_storage_bucket" "functions" {
  name          = "funckle-functions-bucket"
  location      = local.gcp-region
  force_destroy = true

  public_access_prevention = "enforced"
}

resource "google_artifact_registry_repository" "functions" {
  location      = local.gcp-region
  repository_id = "funckle-user-functions"
  description   = "A docker repository for user functions"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false
  }
}


resource "google_service_account" "functions-builder" {
  account_id   = "funckle-functions-builder"
  display_name = "Funckle Functions Builder"
}

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.functions.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.functions-builder.member
}


resource "google_artifact_registry_repository_iam_member" "member" {
  project    = google_artifact_registry_repository.functions.project
  location   = google_artifact_registry_repository.functions.location
  repository = google_artifact_registry_repository.functions.name
  role       = "roles/artifactregistry.writer"
  member     = google_service_account.functions-builder.member
}
