resource "kubernetes_deployment" "django" {
    depends_on = [
        kubernetes_deployment.postgres,
        kubernetes_service.postgres
    ]

  metadata {
    name      = "django-backend"
    namespace = var.namespace
  }
  spec {
    replicas = 1
    wait_for_rollout = false
    selector {
      match_labels = {
        app = "django-backend"
      }
    }
    template {
      metadata {
        labels = {
          app = "django-backend"
        }
      }
      spec {
        container {
          image = var.docker_image_tag
          name  = "django-backend"

          command = [
            "/bin/bash",
            "-c",
            "python manage.py migrate && gunicorn --bind 0.0.0.0:8080 photoupload.wsgi"
          ]

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "200m"
              memory = "256Mi"
            }
          }

          env {
            name  = "DB_HOST"
            value = kubernetes_service.postgres.metadata[0].name
          }
          env {
            name  = "DB_PORT"
            value = "5432"
          }
          env {
            name  = "DB_NAME"
            value = var.db_name
          }
          env {
            name  = "DB_USER"
            value = var.db_user
          }
          env {
            name  = "DB_PASSWORD"
            value = var.db_password
          }

          env {
            name  = "DJANGO_SECRET_KEY"
            value = var.django_secret_key
          }
          env {
            name  = "DEBUG"
            value = "False"
          }
          env {
            name  = "ALLOWED_HOSTS"
            value = var.allowed_hosts
          }
          env {
            name  = "CSRF_TRUSTED_ORIGINS"
            value = var.csrf_trusted_origins
          }
        }
      }
    }
  }
}

# Service
resource "kubernetes_service" "django" {
  metadata {
    name      = "django-backend"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "django-backend"
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

resource "kubernetes_ingress_v1" "django_route" {
  metadata {
    name      = "django-route"
    namespace = var.namespace
  }
  spec {
    rule {
      http {
        path {
          path = "/"
          backend {
            service {
              name = kubernetes_service.django.metadata.0.name
              port {
                number = 8080
              }
            }
          }
        }
      }
    }
  }
}





# HPA
resource "kubernetes_horizontal_pod_autoscaler_v2" "django_hpa" {
  metadata {
    name      = "django-backend-hpa"
    namespace = var.namespace
  }

  spec {
    min_replicas = 1
    max_replicas = 5

    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.django.metadata[0].name
    }

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 50
        }
      }
    }
  }
}