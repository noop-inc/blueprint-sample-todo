import express from 'express'
import { DynamoDBClient, ListTablesCommand } from '@aws-sdk/client-dynamodb'
import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3'

// const TableName = process.env.DYNAMODB_TABLE
const region = process.env.AWS_REGION

const dynamo = new DynamoDBClient({
  endpoint: process.env.DYNAMODB_ENDPOINT,
  signingRegion: region
})
const dynamoCmd = new ListTablesCommand({})
try {
  const results = await dynamo.send(dynamoCmd)
  console.log(results)
} catch (err) {
  console.error(err)
}

const s3 = new S3Client({
  endpoint: process.env.S3_ENDPOINT,
  signingRegion: region
})
const s3Cmd = new ListObjectsV2Command({ Bucket: process.env.S3_BUCKET })
try {
  const results = await s3.send(s3Cmd)
  console.log(results)
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
