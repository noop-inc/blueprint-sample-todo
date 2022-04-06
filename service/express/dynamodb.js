import {
  DynamoDBClient
} from '@aws-sdk/client-dynamodb'
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  DeleteCommand,
  ScanCommand
} from '@aws-sdk/lib-dynamodb'
import { randomUUID } from 'crypto'

const AWSRegion = process.env.AWS_REGION
const DynamoDbEndpoint = process.env.DYNAMODB_ENDPOINT
const DynamoDbTable = process.env.DYNAMODB_TABLE

const dynamoDbClient = new DynamoDBClient({
  endpoint: DynamoDbEndpoint,
  signingRegion: AWSRegion
})

const documentClient = DynamoDBDocumentClient.from(dynamoDbClient)

const sendCommand = async command => await documentClient.send(command)

export const scanTable = async () => {
  const params = {
    TableName: DynamoDbTable
  }
  const command = new ScanCommand(params)
  const data = await sendCommand(command)
  return data.Items
}

export const getItem = async id => {
  const params = {
    TableName: DynamoDbTable,
    Key: {
      id
    }
  }
  const command = new GetCommand(params)
  const data = await sendCommand(command)
  return data.Item
}

export const putItem = async item => {
  const newItem = { id: randomUUID(), ...item }
  const params = {
    TableName: DynamoDbTable,
    Item: newItem
  }
  const command = new PutCommand(params)
  await sendCommand(command)
  return newItem
}

export const deleteItem = async id => {
  const params = {
    TableName: DynamoDbTable,
    Key: {
      id
    }
  }
  const command = new DeleteCommand(params)
  return await sendCommand(command)
}
