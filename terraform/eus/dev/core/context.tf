# This pulls in the global context.
module "ctx" {
    source = "../../../global/context"
    environment = var.environment
}
