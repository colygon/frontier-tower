#!/bin/bash

# Build script for Vercel deployment
echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

echo "Build process completed!"
