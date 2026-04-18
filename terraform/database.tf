resource "kubernetes_persistent_volume_claim" "postgres_pvc" {
  metadata {
    name      = "postgresql-pvc"
    namespace = var.namespace
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
  }
    wait_until_bound = false
}

# PostgreSQL 
resource "kubernetes_deployment" "postgres" {
  metadata {
    name      = "postgresql"
    namespace = var.namespace
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgresql"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgresql"
        }
      }
      spec {
        container {
          image = "registry.redhat.io/rhel9/postgresql-15:latest"
          name  = "postgresql"
          
          env {
            name  = "POSTGRESQL_USER"
            value = var.db_user
          }
          env {
            name  = "POSTGRESQL_PASSWORD"
            value = var.db_password
          }
          env {
            name  = "POSTGRESQL_DATABASE"
            value = var.db_name
          }

          volume_mount {
            name       = "postgresql-data"
            mount_path = "/var/lib/pgsql/data"
          }
        }
        volume {
          name = "postgresql-data"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.postgres_pvc.metadata[0].name
          }
        }
      }
    }
  }
}


resource "kubernetes_service" "postgres" {
  metadata {
    name      = "postgresql"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "postgresql"
    }
    port {
      port        = 5432
      target_port = 5432
    }
  }
}