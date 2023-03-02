import asyncio
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename="server.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


async def handler(reader, writer):

    # Чтение данных от клиента
    addr = writer.get_extra_info('peername')
    logging.info(f"Новое подключение: {addr}")

    data = await reader.read(1024)
    logging.info(f"Получено сообщение: {data.decode()}")

    # Декодирование и обработка данных
    expression = json.loads(data.decode())
    result = eval(expression)

    # Отправка ответа клиенту
    writer.write(json.dumps(result).encode())
    await writer.drain()
    logging.info(f"Отправил сообщение: {result}")

    # Закрытие подключения
    writer.close()
    logging.info(f"Соединение с {addr} закрыто")

async def main():
    server = await asyncio.start_server(handler, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
