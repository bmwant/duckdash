from main import huey

def main():
    tasks = []
    storage = huey.storage
    items = storage.enqueued_items()
    ser = huey.serializer
    for i in items:
        tasks.append(ser.deserialize(i))
    breakpoint()
    print(tasks)


if __name__ == '__main__':
    main()
