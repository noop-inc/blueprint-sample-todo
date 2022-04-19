package com.noop.todosample;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.PutItemResult;
import com.amazonaws.services.dynamodbv2.model.UpdateItemResult;
import com.amazonaws.services.dynamodbv2.model.DeleteItemResult;
// import com.amazonaws.services.dynamodbv2.model.PutItemResult;
// import com.amazonaws.services.dynamodbv2.model.AttributeValue;

// import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PutMapping;

// import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.apache.commons.lang3.RandomStringUtils;
// import org.apache.logging.log4j.Logger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;



class TodoParams extends Object {
    // public String id;
    public String body;
    public List<String> files;

    public String toString() {
        return "<TodoParams> body: " + body + " files: " + files.toString();
    }
}

@RestController
public class TodoController {

    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    @PostMapping("/todos")
    public PutItemResult create(
        @RequestBody TodoParams params
    ) {
        List<String> fileList = new ArrayList<>();

        for (String file: params.files) {
            fileList.add(
                file
            );
        }

        String id = RandomStringUtils.randomAlphanumeric(15);
        logger.info("creating Todo Id" + id +  " using props: " + params.files.toString());
        Todo todo = new Todo(
            id,
            params.body,
            fileList
        );
        DynamoTable dynamo = new DynamoTable("todos");
        Map<String, Object> item = new HashMap<String, Object>();
        item.put("id", todo.getId());
        item.put("body", todo.getBody());
        item.put("files", todo.getFiles());
        logger.info("the item.files value is : " + item.get("files").getClass().toString());
        PutItemResult result = dynamo.putItem(item);
        return result;
    }

    @GetMapping("/api/todos")
    public List<Map<String, Object>> list() {
        logger.info("listing existing Todo records");
        DynamoTable dynamo = new DynamoTable("todos");
        List<Map<String, Object>> items = dynamo.getItems();
        return items;
    }

    @GetMapping("/api/todos/{id}")
    public Map<String, Object> get(@PathVariable String id) {
        logger.info("requested Todo Id: " + id);
        DynamoTable dynamo = new DynamoTable("todos");
        Map<String, Object> item = dynamo.getItem(id);
        return item;
    }

    @DeleteMapping("/api/todos/{id}")
    public DeleteItemResult delete(@PathVariable String id) {
        logger.info("deleting Todo Id: " + id);
        DynamoTable dynamo = new DynamoTable("todos");
        DeleteItemResult result = dynamo.deleteItem(id);
        return result;

    }

    @PutMapping("/api/todos/{id}")
    public UpdateItemResult update(
        @PathVariable String id,
        @RequestBody TodoParams params) {
            Map<String, Object> item = new HashMap<String, Object>();
            logger.info("updating Todo Id: " + id);
            DynamoTable dynamo = new DynamoTable("todos");
            if (params != null && params instanceof TodoParams && ((TodoParams) params).body != null) {
                logger.info(params.body);
                item.put("body", params.body);
            }
            if (params != null && params instanceof TodoParams && ((TodoParams) params).files != null) {
                logger.info(params.files.toString());
                item.put("files", params.files);
            }
            logger.info(params.toString());
            UpdateItemResult result = dynamo.updateItem(id, item);
            logger.info("string version of result..");
            logger.info(result.toString());
            return result;
    }
}
