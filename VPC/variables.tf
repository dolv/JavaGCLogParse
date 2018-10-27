variable vpc_info {
  type = "map"
  default = {
    cidr_block = "10.0.0.0/16"
  }
}
variable subnets_info {
  type = "map"
  default = {
    CIDRs = [
      "10.0.1.0/24",
      "10.0.2.0/24",
      "10.0.3.0/24"
    ]
    AZs = [
      "eu-central-1a",
      "eu-central-1b",
      "eu-central-1c"
    ]
  }
}