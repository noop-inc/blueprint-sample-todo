package com.noop.todosample;

import java.util.ArrayList;
import java.util.Date;

public class Todo {
    private final String id;
    private final String body;
    private final ArrayList<String> files;
    private final Date created;

    public Todo(String id, String body, ArrayList<String> files) {
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

    public ArrayList<String> getFiles() {
        return files;
    }

    public String getCreated() {
        return created.toString();
    }
}
