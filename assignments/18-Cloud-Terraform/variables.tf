variable "aws_region" {
  type        = string
  description = "Target AWS region for deploying cloud infrastructure."
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the Virtual Private Cloud (VPC)."
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  type        = string
  description = "CIDR block for the public subnet within the VPC."
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  type        = string
  description = "EC2 compute instance type."
  default     = "t3.micro"
}

variable "bucket_name" {
  type        = string
  description = "Globally unique name for the S3 object storage bucket."
  default     = "tanishq-cloud-terraform-bucket-24bcs10303"
}

variable "environment" {
  type        = string
  description = "Deployment environment classification (dev, staging, prod)."
  default     = "production"
}

variable "use_localstack" {
  type        = bool
  description = "Enable LocalStack local AWS emulation (set false for real AWS)."
  default     = true
}

variable "localstack_endpoint" {
  type        = string
  description = "Endpoint URL for local LocalStack container emulation."
  default     = "http://127.0.0.1:4566"
}
