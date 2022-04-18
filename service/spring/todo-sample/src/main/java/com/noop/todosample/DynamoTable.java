package com.noop.todosample;

// Util types
// import java.util.ArrayList;
// import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;
import java.util.ArrayList;
// import java.util.Arrays;
// import java.util.Collection;
import java.util.HashMap;

// Service clients
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;

// Document objects
// import com.amazonaws.services.dynamodbv2.document.DynamoDB;
// import com.amazonaws.services.dynamodbv2.document.Table;
// import com.amazonaws.services.dynamodbv2.document.Item;


// models
import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.AttributeAction;
import com.amazonaws.services.dynamodbv2.model.AttributeValueUpdate;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
// import com.fasterxml.jackson.databind.annotation.JsonAppend.Attr;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// import com.amazonaws.services.dynamodbv2.model.ScanResult;
import com.amazonaws.services.dynamodbv2.model.GetItemRequest;
import com.amazonaws.services.dynamodbv2.model.GetItemResult;
import com.amazonaws.services.dynamodbv2.model.PutItemRequest;
import com.amazonaws.services.dynamodbv2.model.PutItemResult;
import com.amazonaws.services.dynamodbv2.model.UpdateItemRequest;
import com.amazonaws.services.dynamodbv2.model.UpdateItemResult;

import com.amazonaws.services.dynamodbv2.model.DeleteItemRequest;
import com.amazonaws.services.dynamodbv2.model.DeleteItemResult;
import com.amazonaws.services.dynamodbv2.model.ReturnConsumedCapacity;
import com.amazonaws.services.dynamodbv2.model.ReturnValue;

// import com.amazonaws.regions.Region;
import com.amazonaws.client.builder.AwsClientBuilder.EndpointConfiguration;
// exceptions
import com.amazonaws.AmazonServiceException;
// import com.amazonaws.AmazonClientException;


/**
 * Class DynamoTable
 * contains DynamoDB functionality in scope for the Todo sample application
 * **/
public class DynamoTable {
    private final Map<String, String> env = System.getenv();
    public final String tableName;
    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);
    public DynamoTable(String tableName) {
        this.tableName = tableName;
    }

    private String getEndpoint() {
        return env.get("DYNAMODB_ENDPOINT");
    }

    private String getRegion() {
        return env.get("AWS_REGION");
    }

    private String getTableName() {
        return env.get("DYNAMODB_TABLE");
    }

    private AmazonDynamoDB getClient() {
        return AmazonDynamoDBClientBuilder
                .standard()
                .withEndpointConfiguration(
                        new EndpointConfiguration(this.getEndpoint(), this.getRegion()))
                // .withRegion("us-east-1")
                .build();
    }

    public List<Map<String, AttributeValue>> getItems() {
        AmazonDynamoDB client = this.getClient();
        ScanRequest request = new ScanRequest().withTableName(this.tableName);
        return client.scan(request).getItems();
    }

    public Map<String, AttributeValue> getItem( String id) {
        AmazonDynamoDB client = this.getClient();
        GetItemRequest request = new GetItemRequest();
        // request.setTableName(this.tableName);
        request.setTableName(this.getTableName());
        request.setReturnConsumedCapacity(ReturnConsumedCapacity.TOTAL);
        request.setProjectionExpression("id, body, files");

        // add primary key to HashMap
        Map<String, AttributeValue> keyMap = new HashMap<>();
        keyMap.put(
            "id",
            new AttributeValue(id)
        );
        request.setKey(keyMap);

        try {
            /*
             * TODO: return clean objects
             * currently returns:
             * [
             *      {
             *          "files": {
             *              "s": null,
             *              ...,
             *              "l": [
             *                      ...
             *                  ]
             *          }
             *      }
             * ]
             * but should be:
             * [
             *      {
             *          id: 'value',
             *          files: [
             *           value,
             *           value,
             *          ]
             *      }
             * ]
             */
            GetItemResult result = client.getItem(request);
            Map<String, AttributeValue> item = result.getItem();

            // try using an entry set or ItemConverter to help clean the item values
            Set<Entry<String, AttributeValue>> entries = item.entrySet();
            for (Entry<String, AttributeValue> entry: entries) {
                logger.info("item key: " + entry.getKey());
                logger.info("item value: " + entry.getValue().toString());
                // entry.getValue()
            }
            return item;

        } catch (AmazonServiceException e) {
             Map<String, AttributeValue> error = new HashMap<>();
             error.put("message", new AttributeValue(e.getErrorMessage()));
             return error;
        }
    }

    public PutItemResult putItem(Map<String, Object> params) {
        AmazonDynamoDB client = this.getClient();

        Map<String, AttributeValue> item = new HashMap<String, AttributeValue>();
        @SuppressWarnings("unchecked")
        /*
            We need to cast params.get("files") from an Object to an ArrayList
            the compiler will warn, but we can ignore it since we know files is an ArrayList defined in our class
        */
        ArrayList<String> requestFiles = (ArrayList<String>)params.get("files");
        // build list Attribute
        List<AttributeValue> itemFiles = new ArrayList<>();
        for (String file: requestFiles) {
            logger.info("add file to itemFiles: " + file);
            itemFiles.add(
                new AttributeValue(file)
            );
        }
        // prepare the Todo to be written
        item.put("id", new AttributeValue(params.get("id").toString()));
        item.put("body", new AttributeValue(params.get("body").toString()));
        item.put("files", new AttributeValue().withL(itemFiles));

        // perform the put request
        PutItemRequest request = new PutItemRequest()
            .withTableName(this.tableName)
            .withItem(item);
        PutItemResult result = client.putItem(request);
        return result;
    }

    public UpdateItemResult updateItem(String id, Map<String, Object> params) {
        logger.info("debugging parameters");
        logger.info(id);
        logger.info(params.toString());
        AmazonDynamoDB client = this.getClient();

        // key Map<String, AttributeValue>
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("id", new AttributeValue(id));

        // attributeUpdates Map<String, AttributeValueUpdate>
        Map<String, AttributeValueUpdate> attributeUpdateValues = new HashMap<String, AttributeValueUpdate>();

        // start request
        UpdateItemRequest request = new UpdateItemRequest()
                .withTableName(this.tableName)
                .withKey(key);

        // if files key is in request params
        if (params.containsKey("files")) {
            @SuppressWarnings("unchecked")
            ArrayList<String> requestFiles = (ArrayList<String>)params.get("files");
            // List<AttributeValue> itemFiles = new ArrayList<>();
            List<AttributeValue> itemFiles = new ArrayList<>();
            for (String file: requestFiles) {
                AttributeValue val = new AttributeValue(file);
                itemFiles.add(val);
            }

            AttributeValue filesValues = new AttributeValue().withL(itemFiles);
            AttributeValueUpdate filesUpdates = new AttributeValueUpdate();
            filesUpdates.setAction("PUT");
            filesUpdates.setValue(filesValues);
            attributeUpdateValues.put("files", filesUpdates);
        }

        // if body key is in request params
        if (params.containsKey("body")) {
            AttributeValue bodyValue = new AttributeValue(params.get("body").toString());
            AttributeValueUpdate bodyUpdates = new AttributeValueUpdate();
            bodyUpdates.setAction("PUT");
            bodyUpdates.setValue(bodyValue);
            attributeUpdateValues.put("body", bodyUpdates);
        }

        // make update request
        request
            .withAttributeUpdates(attributeUpdateValues)
            .withReturnValues(ReturnValue.ALL_NEW);

        UpdateItemResult result = client.updateItem(request);
        logger.info(result.toString());
        return result;
    }

    public DeleteItemResult deleteItem(String id) {
        AmazonDynamoDB client = this.getClient();
        AttributeValue key = new AttributeValue().withS(id);
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("id", key);
        DeleteItemRequest request = new DeleteItemRequest()
            .withTableName(this.tableName)
            .withKey(item);
        DeleteItemResult result = client.deleteItem(request);
        return result;
    }


}
