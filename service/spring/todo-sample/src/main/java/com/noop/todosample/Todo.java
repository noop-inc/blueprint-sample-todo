package com.noop.todosample;


import java.util.Date;
import java.util.List;

public class Todo {
    private final String id;
    private final String body;
    private final List<String> files;
    private final Date created;

    public Todo(String id, String body, List<String> files) {
        this.id = id;
        this.body = body;
        this.files = files;
        this.created = new Date();

    }

    public String getId() {
        return id;
    }

    public String getBody() {
        return body;
    }

    public List<String> getFiles() {
        return files;
    }

    public String getCreated() {
        return created.toString();
    }
}
