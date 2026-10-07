variable "aws_region" {
  type        = string
  description = "AWS region where resources will be provisioned."
  default     = "ap-south-1"
}

variable "bucket_name" {
  type        = string
  description = "Globally unique name for the AWS S3 bucket."
  default     = "tanishq-devops-s3-demo-24bcs10303"
}

variable "localstack_endpoint" {
  type        = string
  description = "Endpoint URL for LocalStack local cloud emulation."
  default     = "http://localhost:4566"
}

variable "environment" {
  type        = string
  description = "Environment deployment tier (dev, staging, prod)."
  default     = "dev"
}
