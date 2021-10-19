from concurrent import futures
import logging
from typing import Text

import grpc
import todo_pb2
import todo_pb2_grpc

class Todo(todo_pb2_grpc.TodoServicer):
    #A list
    store = []

    def createTodo(self, request, context):
        item = todo_pb2.TodoItem(id = len(self.store) + 1, text = request.text)
        self.store.append(item)
        print("Item added to the to do list ", request.text)
        return item

    def readTodos(self, request, context):
        toDoItems = todo_pb2.TodoItems()
        for item in self.store:
            print("Item is being read!!")
            temp = toDoItems.items.add()
            temp.id = item.id
            temp.text = item.text
        return toDoItems

def serve():
    server  = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(Todo(), server)
    server.add_insecure_port('[::]:50051')
    # The server listens to the client here
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()