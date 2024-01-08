variable "environment" {
  description = "Environment tag for the resources"
  type        = string
  default     = "dev"
}

### Container Details
variable "container_name" {
  description = "Name of the container"
  type        = string
  default     = "ops-data-tools"
}

variable "container_image" {
  description = "Container image"
  type        = string
  default     = "ghcr.io/hhs/opre-ops/ops-data-tools"
}

variable "container_tag" {
  description = "Container image tag"
  type        = string
  default     = "118b2835d37dbac932745377e1340498aafc8af1"
}

variable "cpu" {
  description = "CPU requirements. This has specific ration with memory... (beta)"
  type        = number
  default     = 0.25
}

variable "memory" {
  description = "Memory requirements. This has specific ration with cpu... (beta)"
  type        = string
  default     = "0.5Gi"
}
