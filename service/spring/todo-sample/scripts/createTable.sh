#!/usr/bin/env bash

TableName="${1:-todos}"

echo "creating table on local dynamo instance:"
aws dynamodb create-table \
--endpoint-url http://127.0.0.1:8000 \
--region us-east-2 \
--table-name "${TableName}" \
--key-schema AttributeName=id,KeyType=HASH \
--attribute-definitions AttributeName=id,AttributeType=S \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5