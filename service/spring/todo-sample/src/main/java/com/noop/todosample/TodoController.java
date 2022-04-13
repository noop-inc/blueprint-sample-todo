package com.noop.todosample;
import java.util.ArrayList;
// import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
// import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.apache.commons.lang3.RandomStringUtils;



class TodoParams {
    public String body;
    public ArrayList<String> files;
}

@RestController
public class TodoController {

    private static final String id = RandomStringUtils.randomAlphanumeric(15);

    @PostMapping("/todos")
    public Todo create(
        @RequestBody TodoParams params
    ) {
        System.out.println(params.toString());
        return new Todo(
            id,
            params.body,
            params.files
        );
    }

    @GetMapping("/todos")
    public ArrayList<String> getAll() {
        ArrayList<String> todos = new ArrayList<>();
        todos.add("test");
        return todos;
    }
}
