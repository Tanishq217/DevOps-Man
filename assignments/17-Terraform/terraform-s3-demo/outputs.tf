output "bucket_name" {
  description = "The globally unique name of the provisioned AWS S3 bucket."
  value       = aws_s3_bucket.demo_bucket.id
}

output "bucket_arn" {
  description = "The Amazon Resource Name (ARN) of the provisioned S3 bucket."
  value       = aws_s3_bucket.demo_bucket.arn
}

output "bucket_region" {
  description = "The AWS Region hosting the provisioned S3 bucket."
  value       = aws_s3_bucket.demo_bucket.region
}
