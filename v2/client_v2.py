import asyncio
import logging
import json


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        logging.info("Подключился к серверу")

    async def close(self):
        if self.writer is not None:
            self.writer.close()
            await self.writer.wait_closed()

    async def request(self, expression):

        if self.writer is None:
            await self.connect()

        # Отправка запроса
        self.writer.write(json.dumps(expression).encode())
        await self.writer.drain()
        logging.info(f"Отправил сообщение: {expression}")

        # Получение ответа
        data = await self.reader.read(1024)
        result = json.loads(data.decode())
        logging.info(f"Получено сообщение: {result}")

        return result


async def main():
    logging.basicConfig(level=logging.DEBUG, filename="client_v2.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    client = Client('127.0.0.1', 8888)
    try:
        await client.connect()

        expression = input("Введите выражение: ")
        result = await client.request(expression)

        print(f"Результат: {result}")
        logging.info(f"Запрос '{expression}' обработан успешно, результат: {result}")
    except Exception as e:
        logging.error(str(e))
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
