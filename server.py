import grpc
from concurrent import futures
from proto_generated import *


class TaskService(task_service_pb2_grpc.TaskService):
    def __init__(self):
        self.tasks = []

    def CreateTask(self, request, context):
        new_task = task_service_pb2.Task(description=request.description, completed=False)
        self.tasks.append(new_task)
        return new_task

    def GetAllTask(self, request, context):
        for task in self.tasks:
            yield task

    def MarkTaskAsCompleted(self, request, context):
        for task in self.tasks:
            if task.description == request.description:
                task.completed = True
                return task


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_service_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')

    server.start()
    print('Сервер запущен на порту 50051')

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
