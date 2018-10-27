output "vpc_id" {
  value = "${aws_vpc.main.id}"
}

output "security_groups" {
  value = ["${aws_security_group.frontend_web_servers.id}"]
}

output "vpc_subnets_ids" {
  value = "${sort(aws_subnet.frontend.*.id)}"
}

output "vpc_AZs" {
  value = "${sort(distinct(aws_subnet.frontend.*.availability_zone))}"
}