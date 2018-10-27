variable "WebServerCluster" {
  type = "map"
  default = {
    "tomcat1" = "t2.micro"
    "tomcat2" = "t2.micro"
  }
}
variable "region" {}
variable "deployer_key" {}
variable "vpc_id" {}
variable "vpc_subnet_ids" {
  type = "list"
}
variable "vpc_security_group_ids" {
  type = "list"
}
variable "webserver_AZs" {
  type = "list"
}
variable "ssh-private-key-file" {
  default = "~/.ssh/aws_deployer_id_rsa"
}