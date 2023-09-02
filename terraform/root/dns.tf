
resource "google_dns_managed_zone" "env_dns_zone" {
  name        = "funckle"
  description = "Public DNS zone for Funckle"
  dns_name    = "funckle.nerd-extraordinaire.com."
}

resource "google_dns_record_set" "funckle_root" {
  name = google_dns_managed_zone.env_dns_zone.dns_name
  type = "A"
  ttl  = 300

  managed_zone = google_dns_managed_zone.env_dns_zone.name

  rrdatas = [data.kubernetes_service_v1.load_balancer.status.0.load_balancer.0.ingress.0.ip]
}

resource "google_dns_record_set" "funckle_apps" {
  name = "*.${google_dns_managed_zone.env_dns_zone.dns_name}"
  type = "A"
  ttl  = 300

  managed_zone = google_dns_managed_zone.env_dns_zone.name

  rrdatas = [data.kubernetes_service_v1.load_balancer.status.0.load_balancer.0.ingress.0.ip]
}
