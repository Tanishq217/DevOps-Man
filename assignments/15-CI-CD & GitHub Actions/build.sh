#!/bin/bash
set -e

echo "============================================="
echo "  Executing Application Packaging & Build    "
echo "============================================="

# Clean old build directory
rm -rf build
mkdir -p build

# Copy production application files
cp app/calculator.py build/
cp requirements.txt build/

# Generate build metadata file
cat > build/build-info.txt <<EOF
Application: DevOps Calculator CLI
Version: 1.0.0
Build Timestamp: $(date -u '+%Y-%m-%d %H:%M:%SZ')
Git Commit: ${GITHUB_SHA:-"local-build"}
Branch: ${GITHUB_REF_NAME:-"main"}
Build Status: SUCCESS
Artifact Type: Python Packaged Bundle
EOF

echo "Build generated successfully in build/ directory."
echo ""
echo "Artifact Directory Contents:"
ls -la build/
echo ""
cat build/build-info.txt
echo "============================================="
