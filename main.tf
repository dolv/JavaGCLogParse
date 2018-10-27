terraform {
  backend "s3" {
    bucket = "alicetest-tfstate"
    key    = "webservers"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = "${var.region}"
}

resource "aws_key_pair" "deployer" {
  key_name   = "${var.deployer_key["key_name"]}"
  public_key = "${var.deployer_key["public_key"]}"
}

module "vpc" {
  source          = "VPC"
}

module "webserver" {
  source                 = "webserver"
  region                 = "${var.region}"
  vpc_id                 = "${module.vpc.vpc_id}"
  vpc_subnet_ids         = "${module.vpc.vpc_subnets_ids}"
  deployer_key           = "${aws_key_pair.deployer.id}"
  vpc_security_group_ids = "${module.vpc.security_groups}"
  webserver_AZs          = "${module.vpc.vpc_AZs}"
  ssh-private-key-file   = "${var.ssh-private-key-file}"
}


resource "null_resource" "install_tomcat" {
  provisioner "local-exec" {
    command = <<EOT
     ANSIBLE_HOST_KEY_CHECKING=False \
     ansible-playbook install_tomcat.yml \
     -i inventory.yml \
     -u ubuntu \
     -b -vvv\
     -e ansible_ssh_private_key_file=${var.ssh-private-key-file}
EOT
  }
  depends_on = ["module.webserver"]
}