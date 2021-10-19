from __future__ import print_function

import logging
from typing import Text
import grpc
import todo_pb2
import todo_pb2_grpc


def run(toDoItems):
    todoItem = {"id" : 0, "text" : "Finish my homework"}
    channel = grpc.insecure_channel('localhost:50051')
    for item in toDoItems:
        stub = todo_pb2_grpc.TodoStub(channel)
        response = stub.createTodo(item)
        print("In the client!!")
        print("values received from the server id = {} and text = {}"
        .format(response.id, response.text))

def readFromServer():
    channel = grpc.insecure_channel('localhost:50051')
    stub = todo_pb2_grpc.TodoStub(channel)
    response = stub.readTodos(todo_pb2.Empty())
    print("Reading the items from the server!!")
    for item in response.items:
        print("First item is {} and text is {}".format(item.id, item.text)) 

if __name__ == '__main__':
    logging.basicConfig()
    toDoItems = [todo_pb2.TodoItem(id = 1, text = 'Do laundry'), todo_pb2.TodoItem(id = 1, text = 'Do homework'),todo_pb2.TodoItem(id = 1, text = 'Cook food'),todo_pb2.TodoItem(id = 1, text = 'Iron clothes'), todo_pb2.TodoItem(id = 1, text = 'Hit the gym'),todo_pb2.TodoItem(id = 1, text = 'Sleep early')]
    run(toDoItems)
    readFromServer()
