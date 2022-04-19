package com.noop.todosample;

import java.io.InputStream;
import java.util.Map;

// import com.amazonaws.AmazonServiceException;
// import com.amazonaws.regions.Regions;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;

import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.S3ObjectInputStream;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.DeleteObjectRequest;
import com.amazonaws.services.s3.model.UploadObjectRequest;
import com.amazonaws.services.s3.model.PutObjectRequest;


// import com.amazonaws.services.s3.model.UploadPartRequest;
// import com.amazonaws.services.s3.model.UploadPartResult;

/*
https://docs.aws.amazon.com/code-samples/latest/catalog/java-s3-src-main-java-aws-example-s3-HighLevelMultipartUpload.java.html
*/
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManagerBuilder;
import com.amazonaws.services.s3.transfer.Upload;

// import com.amazonaws.regions.Region;
import com.amazonaws.client.builder.AwsClientBuilder.EndpointConfiguration;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class S3Bucket {
    private final Map<String, String> env = System.getenv();
    public final String bucketName;
    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    public S3Bucket(String bucketName) {
        this.bucketName = bucketName;
    }

    public String getEndpoint() {
        return env.getOrDefault("S3_ENDPOINT", "http://127.0.0.1:9000");
    }

    public String getRegion() {
        return env.getOrDefault("AWS_REGION", "us-east-1");
    }

    public String getBucketName() {
        return env.getOrDefault("S3_BUCKET", this.bucketName);
    }

    private AmazonS3 getClient() {
        return AmazonS3ClientBuilder
            .standard()
            .withEndpointConfiguration(
                new EndpointConfiguration(
                    this.getEndpoint(),
                    this.getRegion())
            )
            .build();

    }

    private TransferManager getTransferManager() {
        return TransferManagerBuilder
            .standard()
            .withS3Client(this.getClient())
            .build();
    }

    public S3Object getObject(String key) {
        AmazonS3 client = this.getClient();
        S3Object object = client.getObject(new GetObjectRequest(this.bucketName, key));
        S3ObjectInputStream inputStream = object.getObjectContent();
        logger.info("input stream is a " + inputStream.getClass().toString());
        return object;
    }

    // PutObjectRequest can accept an input stream, but unsure what that translates to in the java world
    public String uploadObject(String name, InputStream file) {
        // getting length of InputStream
        TransferManager tm = this.getTransferManager();
        // tm.upload(
        //     new PutObjectRequest(
        //         bucketName,
        //         name,
        //         file,
        //         new ObjectMetadata()
        //             .setContentLength(file.length);
        //         )
        //     );

        return "";
    }

    public String deleteObject() {
        return "";
    }
}