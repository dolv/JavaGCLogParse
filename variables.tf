variable region {
  default = "eu-central-1"
}

variable deployer_key {
  type = "map"
  default = {
    key_name = "deployer-key"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDJLixTcol7Tmb0MDn2IH/rpnJ0/IOQUwZDPt2UH/wg6uYrGGIWgWMILVW9enWLV9bBk4lOGFaAW8E+QncdIPLXOBOmTQiEsdbU0qTwxz+sR4kwm7nc0XyOOv8Y3WgGPk4WF6a9hMLLKnndQXIBGZPbSxbtoxjwls+zXGYPCMF7Vn00mmzAtvKGd2yZpsWELBfukatSWJcIkS6O5zxmEkGs0l43H9KoniWc2Xu9v9FD522mHSnDHHD2L6cgIEOSveHO4xG4IIm0jFpVnVATjBvSrYtOVa6UBzexarrFMVjAAvVaKYJJdnR6jyZxY1oO7DTtZrH0rIcUvodGZuvM14Bp dudchenkooleksandr@Administrators-MacBook-Pro.local"
  }
}

variable "ssh-private-key-file" {
  default = "~/.ssh/aws_deployer_id_rsa"
}