# =============================================================================
# Session 18: Cloud & Terraform in Action - End-to-End Infrastructure
# Architecture: VPC -> Subnet -> IGW -> Route Table -> SG -> EC2 + S3
# Student: Tanishq | Enrollment: 24bcs10303
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# 1. Virtual Private Cloud (VPC)
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "tanishq-cloud-vpc"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "Cloud-Terraform-Action"
    Owner       = "Tanishq"
    Enrollment  = "24bcs10303"
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. Internet Gateway (IGW)
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "tanishq-cloud-igw"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. Public Subnet
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name        = "tanishq-cloud-public-subnet"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. Route Table & Subnet Association
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "tanishq-cloud-public-rt"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ─────────────────────────────────────────────────────────────────────────────
# 5. Security Group (Web Tier: HTTP, HTTPS, SSH)
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_security_group" "web_sg" {
  name        = "tanishq-cloud-web-sg"
  description = "Security Group allowing inbound HTTP, HTTPS, and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow inbound HTTP on port 80"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow inbound HTTPS on port 443"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow inbound SSH on port 22"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Permit all outbound egress traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "tanishq-cloud-web-sg"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# 6. S3 Storage Bucket with Versioning
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_s3_bucket" "app_storage" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "Cloud-Terraform-Action"
    Owner       = "Tanishq"
    Enrollment  = "24bcs10303"
  }
}

resource "aws_s3_bucket_versioning" "app_storage_versioning" {
  bucket = aws_s3_bucket.app_storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# 7. EC2 Web Server Instance (Demonstrating Explicit & Implicit Dependencies)
# ─────────────────────────────────────────────────────────────────────────────
resource "aws_instance" "web_server" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "<h1>Cloud & Terraform in Action - Tanishq (24bcs10303)</h1>" > /var/www/html/index.html
              EOF

  # Explicit dependency demonstration
  depends_on = [
    aws_internet_gateway.main,
    aws_s3_bucket.app_storage
  ]

  tags = {
    Name        = "tanishq-cloud-web-server"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "Cloud-Terraform-Action"
    Owner       = "Tanishq"
    Enrollment  = "24bcs10303"
  }
}
