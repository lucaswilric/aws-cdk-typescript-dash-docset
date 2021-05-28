#!/bin/bash

mkdir -p aws-cdk-ts.docset/Contents/Resources/Documents/api
cp resources/Info.plist aws-cdk-ts.docset/Contents/Info.plist
cp resources/docSet.dsidx aws-cdk-ts.docset/Contents/Resources/docSet.dsidx

echo Recursively fetching https://docs.aws.amazon.com/cdk/api/latest/typescript/index.html...
wget -nH -np -P tmp -q --recursive --wait 0.2 --random-wait https://docs.aws.amazon.com/cdk/api/latest/typescript/index.html

echo Recursively fetching https://docs.aws.amazon.com/cdk/api/latest/typescript/api/toc.html
wget -nH -np -P tmp -q --recursive --wait 0.2 --random-wait https://docs.aws.amazon.com/cdk/api/latest/typescript/api/toc.html

wget https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html -O tmp/aws-construct-library.html

cp -r tmp/cdk/api/latest/typescript/{fonts,styles} aws-cdk-ts.docset/Contents/Resources/Documents

python gen_docset.py

tar -czf aws-cdk-v${CDK_VERSION}-ts.docset.tar.gz aws-cdk-ts.docset/

# Clean up
rm *.zip
rm -rf tmp/download
