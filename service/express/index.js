import express from 'express'
import { DynamoDBClient, DescribeTableCommand } from '@aws-sdk/client-dynamodb'
import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3'

const AWSRegion = process.env.AWS_REGION

const DynamoDbEndpoint = process.env.DYNAMODB_ENDPOINT
const DynamoDbTable = process.env.DYNAMODB_TABLE

const S3Endpoint = process.env.S3_ENDPOINT
const S3Bucket = process.env.S3_BUCKET

const dynamo = new DynamoDBClient({
  endpoint: DynamoDbEndpoint,
  signingRegion: AWSRegion
})
const dynamoDbCmd = new DescribeTableCommand({
  TableName: DynamoDbTable
})
try {
  const results = await dynamo.send(dynamoDbCmd)
  console.log(JSON.stringify(results))
} catch (err) {
  console.error(err)
}

const s3 = new S3Client({
  endpoint: S3Endpoint
})
const s3Cmd = new ListObjectsV2Command({
  Bucket: S3Bucket
})
try {
  const results = await s3.send(s3Cmd)
  console.log(JSON.stringify(results))
} catch (err) {
  console.error(err)
}

const app = express()

app.use(express.json())

app.use('/api', (req, res) => {
  res.json({ data: 'hello world' })
})

const port = process.env.PORT || 80
const server = app.listen(port, err =>
  console[err ? 'error' : 'log'](err || `server running on ${port}`)
)

process.once('SIGTERM', () => {
  console.log('SIGTERM received')
  server.close(err => {
    console[err ? 'error' : 'log'](err || 'Server closed')
    process.exit(err ? 1 : 0)
  })
})
