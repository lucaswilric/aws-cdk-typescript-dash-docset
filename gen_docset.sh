#!/bin/bash

CDK_VERSION=1.106.1
ARCHIVE_NAME=aws-cdk-typescript-docs-${CDK_VERSION}

mkdir -p aws-cdk-ts.docset/Contents/Resources/Documents/api
cp resources/Info.plist aws-cdk-ts.docset/Contents/Info.plist
cp resources/docSet.dsidx aws-cdk-ts.docset/Contents/Resources/docSet.dsidx

echo "Getting docs from GitHub..."
wget https://github.com/aws/aws-cdk/releases/download/v${CDK_VERSION}/${ARCHIVE_NAME}.zip

mkdir -p tmp
unzip -qqd tmp/download ${ARCHIVE_NAME}.zip

cp -r tmp/download/{fonts,styles} aws-cdk-ts.docset/Contents/Resources/Documents

python gen_docset.py

tar -czf aws-cdk-v${CDK_VERSION}-ts.docset.tar.gz aws-cdk-ts.docset/

# Clean up
rm *.zip
rm -rf tmp/download
