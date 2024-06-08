# create the ZenServer deployment
resource "kubernetes_namespace" "zen-server" {
  metadata {
    name = "${var.name}-${var.namespace}"
  }
}

resource "helm_release" "zen-server" {

  name      = "${var.name}-zenmlserver"
  chart     = var.helm_chart
  namespace = kubernetes_namespace.zen-server.metadata[0].name

  set {
    name  = "zenml.image.repository"
    value = var.zenmlserver_image_repo
  }  
  set {
    name = "zenml.image.tag"
    value = var.zenmlserver_image_tag
  }
  set {
    name  = "zenml.deploymentType"
    value = "azure"
  }

  set {
    name  = "zenml.secretsStore.type"
    value = "azure"
  }
  set {
    name  = "zenml.secretsStore.azure.key_vault_name"
    value = azurerm_key_vault.secret_manager.name
  }

  set {
    name = "zenml.analyticsOptIn"
    value = var.analytics_opt_in
  }
  
  # set up the right path for ZenML
  set {
    name  = "zenml.ingress.annotations.nginx\\.ingress\\.kubernetes\\.io/rewrite-target"
    value = ""
  }
  set {
    name  = "zenml.ingress.host"
    value = var.create_ingress_controller ? "zenml.${data.kubernetes_service.ingress-controller[0].status.0.load_balancer.0.ingress.0.ip}.nip.io" : "zenml.${var.ingress_controller_ip}.nip.io"
  }
  set {
    name  = "zenml.ingress.tls.enabled"
    value = var.ingress_tls
  }
  set {
    name  = "zenml.ingress.tls.generateCerts"
    value = var.ingress_tls_generate_certs
  }
  set {
    name  = "zenml.ingress.tls.secretName"
    value = "${var.name}-${var.ingress_tls_secret_name}"
  }

  # set parameters for the mysql database
  set {
    name  = "zenml.database.url"
    value = var.deploy_db ? "mysql://${var.database_username}:${azurerm_mysql_flexible_server.mysql[0].administrator_password}@${azurerm_mysql_flexible_server.mysql[0].name}.mysql.database.azure.com:3306/${var.db_name}" : var.database_url
  }
  set {
    name  = "zenml.database.sslCa"
    value = var.deploy_db ? "" : var.database_ssl_ca
  }
  set {
    name  = "zenml.database.sslCert"
    value = var.deploy_db ? "" : var.database_ssl_cert
  }
  set {
    name  = "zenml.database.sslKey"
    value = var.deploy_db ? "" : var.database_ssl_key
  }
  set {
    name  = "zenml.database.sslVerifyServerCert"
    value = var.deploy_db ? false : var.database_ssl_verify_server_cert
  }
  depends_on = [
    resource.kubernetes_namespace.zen-server
  ]
}

data "kubernetes_secret" "certificates" {
  metadata {
    name      = "${var.name}-${var.ingress_tls_secret_name}"
    namespace = "${var.name}-${var.namespace}"
  }
  binary_data = {
    "tls.crt" = ""
    "tls.key" = ""
    "ca.crt"  = ""
  }

  depends_on = [
    helm_release.zen-server
  ]
}