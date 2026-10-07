output "vpc_id" {
  description = "The ID of the provisioned Virtual Private Cloud (VPC)."
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "The ID of the provisioned public subnet."
  value       = aws_subnet.public.id
}

output "internet_gateway_id" {
  description = "The ID of the attached Internet Gateway."
  value       = aws_internet_gateway.main.id
}

output "security_group_id" {
  description = "The ID of the web security group."
  value       = aws_security_group.web_sg.id
}

output "instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.web_server.id
}

output "instance_private_ip" {
  description = "The private IPv4 address assigned to the EC2 instance."
  value       = aws_instance.web_server.private_ip
}

output "instance_public_ip" {
  description = "The public IPv4 address assigned to the EC2 instance."
  value       = aws_instance.web_server.public_ip
}

output "s3_bucket_name" {
  description = "The globally unique name of the S3 storage bucket."
  value       = aws_s3_bucket.app_storage.id
}

output "s3_bucket_arn" {
  description = "The Amazon Resource Name (ARN) of the S3 storage bucket."
  value       = aws_s3_bucket.app_storage.arn
}
