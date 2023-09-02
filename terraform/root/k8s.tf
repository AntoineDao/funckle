resource "google_service_account" "default" {
  account_id   = "k8s-node-default"
  display_name = "Kubernetes Node Default Service Account"
}


resource "google_artifact_registry_repository_iam_member" "k8s_node" {
  project    = google_artifact_registry_repository.functions.project
  location   = google_artifact_registry_repository.functions.location
  repository = google_artifact_registry_repository.functions.name
  role       = "roles/artifactregistry.reader"
  member     = google_service_account.default.member

}


resource "google_project_iam_member" "k8s_node_logging" {
  project = data.google_project.project.project_id
  role    = "roles/logging.logWriter"
  member  = google_service_account.default.member
}

resource "google_container_cluster" "primary" {
  name     = "funckle-cluster"
  location = local.gcp-zone

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # private_cluster_config {
  #   # enable_private_nodes = false
  #   # master_ipv4_cidr_block = "172.16.0.32/28"
  # }
  logging_config {
    enable_components = ["WORKLOADS", "SYSTEM_COMPONENTS"]
  }

  ip_allocation_policy {}
  workload_identity_config {
    workload_pool = "${data.google_project.project.project_id}.svc.id.goog"
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "default-node-pool"
  location   = local.gcp-zone
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    preemptible  = true
    machine_type = "e2-standard-2"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}


data "kubernetes_service_v1" "load_balancer" {
  metadata {
    name      = "kourier"
    namespace = "kourier-system"
  }
}


module "my-app-workload-identity" {
  source              = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  use_existing_k8s_sa = true
  annotate_k8s_sa     = false
  name                = "funckle-server"
  namespace           = "funckle"
  project_id          = data.google_project.project.project_id
  roles               = ["roles/storage.admin", "roles/logging.viewer"]
}
