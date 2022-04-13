package com.noop.todosample;

// data types
// import java.util.ArrayList;
// import java.util.Arrays;
import java.util.List;
import java.util.Map;
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
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
// import com.amazonaws.services.dynamodbv2.model.ScanResult;
import com.amazonaws.services.dynamodbv2.model.GetItemRequest;
import com.amazonaws.services.dynamodbv2.model.GetItemResult;
import com.amazonaws.services.dynamodbv2.model.PutItemRequest;
import com.amazonaws.services.dynamodbv2.model.PutItemResult;
// import com.amazonaws.services.dynamodbv2.model.DeleteItemRequest;
// import com.amazonaws.services.dynamodbv2.model.DeleteItemResult;
import com.amazonaws.services.dynamodbv2.model.ReturnConsumedCapacity;
import com.amazonaws.services.dynamodbv2.model.ReturnValue;

// exceptions
import com.amazonaws.AmazonServiceException;
// import com.amazonaws.AmazonClientException;

public class DynamoTable {
    public final String tableName;
    public DynamoTable(String tableName) {
        this.tableName = tableName;
    }

    private AmazonDynamoDB getClient() {
        return AmazonDynamoDBClientBuilder.standard().build();
    }

    public List<Map<String, AttributeValue>> getItems() {
        AmazonDynamoDB client = this.getClient();
        ScanRequest request = new ScanRequest().withTableName(this.tableName);
        return client.scan(request).getItems();
    }

    public Map<String, AttributeValue> getItem( String id) {
        AmazonDynamoDB client = this.getClient();
        GetItemRequest request = new GetItemRequest();
        request.setTableName(this.tableName);
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
            GetItemResult result = client.getItem(request);
            return result.getItem();
        } catch (AmazonServiceException e) {
             Map<String, AttributeValue> error = new HashMap<>();
             error.put("message", new AttributeValue(e.getErrorMessage()));
             return error;
        }
    }

    public PutItemResult putItem(Map<String, Object> params) {
        AmazonDynamoDB client = this.getClient();
        Map<String, AttributeValue> item = new HashMap<String, AttributeValue>();
        item.put("id", new AttributeValue(params.get("id").toString()));
        item.put("body", new AttributeValue(params.get("body").toString()));
        PutItemRequest request = new PutItemRequest()
            .withTableName(this.tableName)
            .withItem(item)
            .withReturnValues(ReturnValue.ALL_NEW);
        PutItemResult result = client.putItem(request);
        return result;
    }
}
