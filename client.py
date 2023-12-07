import grpc
from proto_generated import *
from google.protobuf import empty_pb2


def create_task(stub, description):
    task = task_service_pb2.Task(description=description, completed=False)
    response = stub.CreateTask(task)
    print(f'Создана новая задача: {response.description}')


def get_all_tasks(stub):
    print('Все задачи:')
    for task in stub.GetAllTask(empty_pb2.Empty()):
        print(f' - {task.description} выполнение: {task.completed}')


def mark_task_as_completed(stub, description):
    task = task_service_pb2.Task(description=description, completed=True)
    response = stub.MarkTaskAsCompleted(task)
    print(f'{task.description} помечено как выполненная задача')


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_service_pb2_grpc.TaskServiceStub(channel)

        # TODO: добавить UI

        create_task(stub, 'Научиться жить правильно')
        create_task(stub, 'Потыкаться в gRPC')
        get_all_tasks(stub)
        mark_task_as_completed(stub, 'Потыкаться в gRPC')
        get_all_tasks(stub)


if __name__ == '__main__':
    run()
