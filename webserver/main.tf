data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}


resource "aws_instance" "web" {
  count = "${length(keys(var.WebServerCluster))}"
  ami = "${data.aws_ami.ubuntu.id}"
  instance_type = "${lookup(var.WebServerCluster,element(keys(var.WebServerCluster), count.index))}"
  key_name = "${var.deployer_key}"
  subnet_id = "${element(var.vpc_subnet_ids, count.index)}"
  vpc_security_group_ids = ["${var.vpc_security_group_ids}"]
  associate_public_ip_address = true
  user_data =<<EOT
#!/usr/bin/env bash
apt install -y python3
ln -s $(which python3) /usr/bin/python
EOT

  tags {
    Name = "webserver"
  }
}

data "aws_elb_service_account" "main" {}

resource "aws_s3_bucket" "elb_logs" {
  bucket = "hometask-elb-access-logs"
  region = "${var.region}"
  acl    = "private"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:PutObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::hometask-elb-access-logs/*",
      "Principal": {
        "AWS": [
          "${data.aws_elb_service_account.main.arn}"
        ]
      }
    }
  ]
}
POLICY
}

resource "aws_elb" "frontend_elb" {
  name               = "frontend-terraform-elb"
  subnets            = ["${var.vpc_subnet_ids}"]
  security_groups    = ["${var.vpc_security_group_ids}"]
  depends_on = ["aws_s3_bucket.elb_logs"]

  access_logs {
    bucket        = "${aws_s3_bucket.elb_logs.bucket}"
    bucket_prefix = "elb-access-logs"
    interval      = 5
  }

  listener {
    instance_port     = 8080
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

//  listener {
//    instance_port      = 8443
//    instance_protocol  = "http"
//    lb_port            = 443
//    lb_protocol        = "https"
//    ssl_certificate_id = "arn:aws:iam::123456789012:server-certificate/certName"
//  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "HTTP:8080/"
    interval            = 10
  }

  instances                   = ["${aws_instance.web.*.id}"]
  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400

  tags {
    Name = "frontend-terraform-elb"
  }
}

resource "null_resource" "generate_inventory" {
  triggers {
    _ = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<EOT
      echo "${join("\n", aws_instance.web.*.public_ip)}" > inventory.yml
EOT
  }
  depends_on = ["aws_instance.web"]
}

resource "null_resource" "wait_vm_ready" {
  count = "${aws_instance.web.count}"

  provisioner "remote-exec" {
    connection {
      host        = "${element(aws_instance.web.*.public_ip, count.index)}"
      user        = "ubuntu"
      private_key = "${file(var.ssh-private-key-file)}"
      timeout     = 900
    }

    inline = [
      "echo 'successfully connected to ${element(aws_instance.web.*.public_ip, count.index)}'",
    ]
  }
  depends_on = ["null_resource.generate_inventory"]
}