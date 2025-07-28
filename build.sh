#!/bin/bash
# Build script for Round 1A

echo "🚀 Building Adobe Hackathon Round 1A - PDF Outline Extraction"

# Build Docker image
docker build --platform linux/amd64 -t round1a:latest .

echo "✅ Round 1A build complete!"
echo "To run: docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output --network none round1a:latest"
