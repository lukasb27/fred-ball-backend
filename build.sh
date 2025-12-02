#!/bin/bash
set -e

### CONFIG ###
APP_DIR="app"                # your python package folder
PYTHON_VERSION="3.13"        # must match your Lambda runtime
ARCH="arm64"                 # or "x86_64"
################

echo "==> Cleaning old build..."
rm -rf package deployment.zip requirements.txt

echo "==> Exporting Poetry dependencies..."
poetry export -f requirements.txt --without-hashes -o requirements.txt

echo "==> Creating package directory..."
mkdir package

echo "==> Installing dependencies inside Lambda Docker image..."

if [ "$ARCH" == "arm64" ]; then
  DOCKER_PLATFORM="--platform=linux/arm64"
else
  DOCKER_PLATFORM="--platform=linux/amd64"
fi

docker run $DOCKER_PLATFORM \
  --entrypoint /bin/bash \
  -v "$(pwd)":/var/task \
  -w /var/task \
  --rm public.ecr.aws/lambda/python:${PYTHON_VERSION} \
  -c "pip install -r requirements.txt -t package"

echo "==> Copying FastAPI app code..."
cp -R ${APP_DIR} package/

echo "==> Checking for macOS binary contamination..."

BAD_FILES=$(find package -name "*.so" | grep -E "darwin|macos" || true)

if [ ! -z "$BAD_FILES" ]; then
  echo "❌ ERROR: macOS .so files detected — Lambda cannot load these:"
  echo "$BAD_FILES"
  echo ""
  echo "This means dependencies were installed outside Docker."
  echo "Remove 'package/' and run this script again."
  exit 1
fi

echo "==> Packaging deployment.zip..."
cd package
zip -r ../deployment.zip .
cd ..
rm -rf package/

echo "==> 🎉 Build complete!"
echo "Generated: deployment.zip"
echo "Upload to Lambda with handler: ${APP_DIR}.main.handler"
