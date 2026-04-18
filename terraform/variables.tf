variable "openshift_server_url" {
  type        = string
  description = "OpenShift sandbox url"
}

variable "openshift_token" {
  type        = string
  description = "OpenShift access/login token"
  sensitive   = true
}

variable "namespace" {
  type        = string
  description = "namespace"
}

variable "docker_image_tag" {
  type        = string
  description = "docker image name"
}

variable "github_username" {
  type        = string
  description = "username"
}

variable "github_token" {
  type        = string
  description = "GitHub PAT"
  sensitive   = true
}

variable "django_secret_key" {
  type        = string
  description = "Django key"
  sensitive   = true
}

variable "db_name" {
  type        = string
  description = "db_name"
}

variable "db_user" {
  type        = string
  description = "db_user"
}

variable "db_password" {
  type        = string
  description = "db_password"
  sensitive   = true
}