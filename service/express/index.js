import express from 'express'
import morgan from 'morgan'
import { randomUUID } from 'crypto'
import { DynamoDBClient, PutItemCommand } from '@aws-sdk/client-dynamodb'
// import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3'

const AWSRegion = process.env.AWS_REGION

const DynamoDbEndpoint = process.env.DYNAMODB_ENDPOINT
const DynamoDbTable = process.env.DYNAMODB_TABLE

// const S3Endpoint = process.env.S3_ENDPOINT
// const S3Bucket = process.env.S3_BUCKET

const dynamoDbClient = new DynamoDBClient({
  endpoint: DynamoDbEndpoint,
  signingRegion: AWSRegion
})
// const dynamoDbCmd = new DescribeTableCommand({
//   TableName: DynamoDbTable
// })
// try {
//   const results = await dynamo.send(dynamoDbCmd)
//   console.log(JSON.stringify(results))
// } catch (err) {
//   console.error(err)
// }

// const s3 = new S3Client({
//   endpoint: S3Endpoint
// })
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
//   attachment: null,
//   completed: true || false,
//   deleted: true || false
// }

const app = express()
app.use(express.json())
app.use(morgan('tiny'))

// app.get('/favicon.ico', (req, res) => {
//   res.status(204).end()
// })

// app.get('/api/test', (req, res) => {
//   res.json({ data: 'hello world' })
// })

// all todos
app.get('/api/todos', (req, res) => {
  res.json({ data: 'all todos' })
})

// new todo
app.post('/api/todos', async (req, res) => {
  const body = req.body
  const description = body.description
  const newTodo = {
    id: randomUUID(),
    description,
    created: Date.now(),
    completed: false,
    deleted: false
  }

  const params = {
    TableName: DynamoDbTable,
    Item: {
      id: { S: newTodo.id },
      description: { S: newTodo.description },
      created: { N: newTodo.created },
      completed: { BOOL: newTodo.completed },
      deleted: { BOOL: newTodo.deleted }
    }
  }

  const command = new PutItemCommand(params)

  const data = await dynamoDbClient.send(command)
  console.log(data)

  res.json({ data })
})

// get todo
app.get('/api/todos/:todoId', (req, res) => {
  const params = req.params
  const todoId = params.todoId
  res.json({ data: `get todoId ${todoId}` })
})

// update todo
app.put('/api/todos/:todoId', (req, res) => {
  const params = req.params
  const todoId = params.todoId
  // const body = res.body
  res.json({ data: `update todoId ${todoId}` })
})

// update todo
app.delete('/api/todos/:todoId', (req, res) => {
  const params = req.params
  const todoId = params.todoId
  res.json({ data: `delete todoId ${todoId}` })
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
