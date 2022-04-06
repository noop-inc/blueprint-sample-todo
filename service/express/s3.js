import {
  S3Client,
  GetObjectCommand,
  DeleteObjectCommand
} from '@aws-sdk/client-s3'
import { Upload } from '@aws-sdk/lib-storage'
import { extension } from 'mime-types'
import { randomUUID } from 'crypto'

const S3Endpoint = process.env.S3_ENDPOINT
const S3Bucket = process.env.S3_BUCKET

const s3Client = new S3Client({
  endpoint: S3Endpoint
})

const sendCommand = async command => await s3Client.send(command)

export const getObject = async key => {
  const params = {
    Bucket: S3Bucket,
    Key: key
  }
  const command = new GetObjectCommand(params)
  const data = await sendCommand(command)
  return data.Body
}

export const uploadObject = async ({ buffer, mimetype }) => {
  const ext = extension(mimetype)
  const id = randomUUID()
  const key = `${id}.${ext}`
  const params = {
    Bucket: S3Bucket,
    Key: key,
    Body: buffer,
    ContentType: mimetype
  }
  const upload = new Upload({
    client: s3Client,
    params
  })
  await upload.done()
  return key
}

export const deleteObject = async key => {
  const params = {
    Bucket: S3Bucket,
    Key: key
  }
  const command = new DeleteObjectCommand(params)
  const data = await sendCommand(command)
  return data
}
