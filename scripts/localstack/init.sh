#!/bin/bash

# LocalStack initialization script for AI4U Backend
# This script runs when LocalStack is ready and creates required AWS resources.

echo "======================================"
echo "Initializing LocalStack AWS resources for AI4U Backend..."
echo "======================================"

# Configure AWS CLI for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export ENDPOINT_URL="http://localhost:4566"

# Wait for LocalStack to be fully ready
echo "Waiting for LocalStack to be fully ready..."
sleep 5

echo ""
echo "======================================"
echo "Creating LocalStack SQS queue..."
echo "======================================"
echo ""

QUEUE_NAME="localstack-queue"
echo "Creating queue: ${QUEUE_NAME}"
awslocal sqs create-queue --queue-name "${QUEUE_NAME}" 2>/dev/null || true

echo ""
echo "======================================"
echo "LocalStack initialization complete!"
echo "======================================"
echo ""
echo "To verify queue, run:"
echo "  docker compose exec localstack awslocal sqs list-queues"
echo ""
