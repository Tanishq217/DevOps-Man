# =============================================================================
# Terraform S3 Demo - AWS S3 Bucket Resource Definition
# Student: Tanishq | Enrollment: 24bcs10303
# =============================================================================

resource "aws_s3_bucket" "demo_bucket" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "DevOps-IaC-Demo"
    Owner       = "Tanishq"
    Enrollment  = "24bcs10303"
  }
}

# Optional S3 bucket versioning configuration
resource "aws_s3_bucket_versioning" "demo_bucket_versioning" {
  bucket = aws_s3_bucket.demo_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}
