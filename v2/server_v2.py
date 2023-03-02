import asyncio
import logging
import json


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def start(self):
        server = await asyncio.start_server(self.handler, self.host, self.port)
        logging.basicConfig(level=logging.DEBUG, filename="server_v2.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")
        async with server:
            await server.serve_forever()

    async def handler(self, reader, writer):

        # Чтение данных от клиента
        addr = writer.get_extra_info('peername')
        logging.info(f"Новое подключение: {addr}")

        data = await reader.read(1024)
        logging.info(f"Получено сообщение: {data.decode()}")

        # Декодирование и обработка данных
        expression = json.loads(data.decode())
        result = self.eval_exp(expression)

        # Отправка ответа клиенту
        writer.write(json.dumps(result).encode())
        await writer.drain()
        logging.info(f"Отправил сообщение: {result}")

        # Закрытие подключения
        writer.close()
        logging.info(f"Соединение с {addr} закрыто")

    def eval_exp(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            logging.error(str(e))
            return None


if __name__ == '__main__':
    server = Server('127.0.0.1', 8888)
    asyncio.run(server.start())
