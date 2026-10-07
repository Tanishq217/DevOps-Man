output "vpc_id" {
  description = "ID of the provisioned VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "security_group_id" {
  description = "Security group ID allowing web and API traffic"
  value       = aws_security_group.app_sg.id
}

output "ec2_instance_id" {
  description = "EC2 instance ID hosting the TaskBoard server"
  value       = aws_instance.app_server.id
}

output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "s3_bucket_name" {
  description = "S3 bucket name for deployment artifacts"
  value       = aws_s3_bucket.artifacts.id
}
