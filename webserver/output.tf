output "servers_ips" {
  value = "${aws_instance.web.*.public_ip}"
}
