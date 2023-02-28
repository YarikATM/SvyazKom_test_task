import asyncio
import logging
import json

logging.basicConfig(level=logging.DEBUG, filename="client.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


async def client(expression):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        logging.info("Подключился к серверу")

        # Отправка запроса
        request = expression
        writer.write(json.dumps(request).encode())
        await writer.drain()
        logging.info(f"Отправил сообщение: {expression}")

        # Получение ответа
        data = await reader.read(1024)
        response = json.loads(data.decode())
        logging.info(f"Получено сообщение: {response}")

        # Закрытие подключения
        writer.close()

        return response

    except Exception as e:
        logging.error(str(e))
        return None


if __name__ == "__main__":
    exp = input("Введите выражение:")
    result = asyncio.run(client(exp))
    print(f"Результат: {result}")
    logging.info(f"Результат: {result}")
