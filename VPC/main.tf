resource "aws_vpc" "main" {
  cidr_block = "${var.vpc_info["cidr_block"]}"
  enable_dns_hostnames = true

  tags {
    Name = "main"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = "${aws_vpc.main.id}"

  tags {
    Name = "main"
  }
}

resource "aws_route_table" "r" {
  vpc_id = "${aws_vpc.main.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gw.id}"
  }

  tags {
    Name = "Internet"
  }
}

resource "aws_subnet" "frontend" {
  vpc_id     = "${aws_vpc.main.id}"
  count = "${length(var.subnets_info["CIDRs"])}"
  availability_zone = "${element(var.subnets_info["AZs"], count.index)}"
  cidr_block = "${element(var.subnets_info["CIDRs"], count.index)}"

  tags {
    Name = "frontend"
  }
}

resource "aws_route_table_association" "a" {
  count = "${length(var.subnets_info["CIDRs"])}"
  subnet_id      = "${element(sort(aws_subnet.frontend.*.id), count.index)}"
  route_table_id = "${aws_route_table.r.id}"
}

resource "aws_security_group" "frontend_web_servers" {
  vpc_id = "${aws_vpc.main.id}"

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
  }

  ingress {
    cidr_blocks = ["${var.vpc_info["cidr_block"]}"]
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"

  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}