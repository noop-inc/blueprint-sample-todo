import express from 'express'
import multer from 'multer'
import morgan from 'morgan'
import { randomUUID } from 'crypto'
import { extension, lookup } from 'mime-types'
import cors from 'cors'

import {
  DynamoDBClient
} from '@aws-sdk/client-dynamodb'

import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  UpdateCommand,
  DeleteCommand,
  ScanCommand
} from '@aws-sdk/lib-dynamodb'

import {
  S3Client,
  ListObjectsV2Command,
  GetObjectCommand,
  DeleteObjectCommand
} from '@aws-sdk/client-s3'
import { Upload } from '@aws-sdk/lib-storage'

const AWSRegion = process.env.AWS_REGION

const DynamoDbEndpoint = process.env.DYNAMODB_ENDPOINT
const DynamoDbTable = process.env.DYNAMODB_TABLE

const S3Endpoint = process.env.S3_ENDPOINT
const S3Bucket = process.env.S3_BUCKET

const dynamoClient = new DynamoDBClient({
  endpoint: DynamoDbEndpoint,
  signingRegion: AWSRegion
})

const dynamoDb = DynamoDBDocumentClient.from(dynamoClient)

// const dynamoDbCmd = new DescribeTableCommand({
//   TableName: DynamoDbTable
// })
// try {
//   const results = await dynamo.send(dynamoDbCmd)
//   console.log(JSON.stringify(results))
// } catch (err) {
//   console.error(err)
// }

const s3 = new S3Client({
  endpoint: S3Endpoint
})

// const s3Cmd = new ListObjectsV2Command({
//   Bucket: S3Bucket
// })
// try {
//   const results = await s3.send(s3Cmd)
//   console.log(JSON.stringify(results))
// } catch (err) {
//   console.error(err)
// }

// const exampleTo = {
//   id: 'unique id',
//   created: Date.now(),
//   description: 'foo bar',
//   images: [],
//   completed: true || false,
//   deleted: true || false
// }

const app = express()
app.use(cors())
app.use(express.json())
app.use(morgan('tiny'))

const storage = multer.memoryStorage()
const upload = multer({
  storage,
  limits: {
    fileSize: 1000000,
    files: 6
  }
})
const uploader = upload.array('images', 6)

app.get('/favicon.ico', (req, res) => {
  res.status(204).end()
})

// app.get('/api/test', (req, res) => {
//   res.json({ data: 'hello world' })
// })

// all todos
app.get('/api/todos', async (req, res) => {
  const params = {
    TableName: DynamoDbTable
  }
  const command = new ScanCommand(params)
  const data = await dynamoDb.send(command)
  res.json(data.Items)
})

// images
app.get('/api/images/:imageId', async (req, res) => {
  const params = req.params
  const imageId = params.imageId
  const s3Command = new GetObjectCommand({
    Bucket: S3Bucket,
    Key: imageId
  })
  const data = await s3.send(s3Command)
  const stream = data.Body
  const contentType = stream.headers['content-type'] || lookup(imageId)
  if (contentType) res.setHeader('Content-Type', contentType)
  stream.pipe(res)
})

// new todo
app.post('/api/todos', uploader, async (req, res) => {
  const images = []
  for (const file of (req?.files || [])) {
    const ext = extension(file.mimetype)
    const id = randomUUID()
    const objectName = `${id}.${ext}`
    const params = {
      Bucket: S3Bucket,
      Key: objectName,
      Body: file.buffer,
      ContentType: file.mimetype
    }
    const parallelUploads3 = new Upload({
      client: s3,
      params
    })
    parallelUploads3.on('httpUploadProgress', (progress) => {
      console.log(progress)
    })
    await parallelUploads3.done()
    images.push(objectName)
  }
  const body = req.body
  const description = body.description
  const newTodo = {
    id: randomUUID(),
    description,
    created: Date.now(),
    completed: false
  }
  if (images.length) newTodo.images = images
  const params = {
    TableName: DynamoDbTable,
    Item: newTodo
  }
  const command = new PutCommand(params)
  await dynamoDb.send(command)
  res.json(newTodo)
})
// get todo
app.get('/api/todos/:todoId', async (req, res) => {
  const params = req.params
  const todoId = params.todoId
  const command = new GetCommand({
    TableName: DynamoDbTable,
    Key: {
      primaryKey: todoId
    }
  })
  const data = await dynamoDb.send(command)
  res.json(data.Item)
})

// update todo
app.put('/api/todos/:todoId', async (req, res) => {
  const params = req.params
  const todoId = params.todoId
  res.json({ data: `update todoId ${todoId}` })
})

// delete todo
app.delete('/api/todos/:todoId', (req, res) => {
  const params = req.params
  const todoId = params.todoId
  res.json({ data: `delete todoId ${todoId}` })
})

const port = 3000
const server = app.listen(port, err =>
  console[err ? 'error' : 'log'](err || `Server running on ${port}`)
)

process.once('SIGTERM', () => {
  console.log('SIGTERM received')
  server.close(err => {
    console[err ? 'error' : 'log'](err || 'Server closed')
    process.exit(err ? 1 : 0)
  })
})
