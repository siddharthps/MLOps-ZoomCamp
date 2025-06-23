# run_integration_test.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Building Docker image..."
docker build -t my_batch_image .

# Check if Localstack container is running
$localstackRunning = docker ps --format '{{.Names}}' | Select-String -Pattern '^localstack_main$'

if (-not $localstackRunning) {
    Write-Host "Starting Localstack container..."
    docker-compose up -d localstack
    Write-Host "Waiting 10 seconds for Localstack to be ready..."
    Start-Sleep -Seconds 10
} else {
    Write-Host "Localstack already running."
}

Write-Host "Creating S3 bucket 'nyc-duration' if not exists..."
try {
    aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration > $null 2>&1
} catch {
    Write-Host "Bucket not found. Creating bucket..."
    aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
}

Write-Host "Running integration test inside Docker container..."
docker run --rm `
    -e AWS_ACCESS_KEY_ID=test `
    -e AWS_SECRET_ACCESS_KEY=test `
    -e AWS_DEFAULT_REGION=us-east-1 `
    -e S3_ENDPOINT_URL=http://host.docker.internal:4566 `
    -e INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet" `
    -e OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet" `
    my_batch_image `
    python integration_test.py

Write-Host "Integration test completed."
