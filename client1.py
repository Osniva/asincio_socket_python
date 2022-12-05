import asyncio
import os

HOST = "localhost"
PORT = 2001

async def run_cliend(reader, writer):
    
    
    data = None
    print("Чекаю коли щось отримаю")
    data = await reader.read()
    print(data)
    name_file = data.decode()
    print(name_file)
    file = open(name_file, 'wb')
    
    while data != b"end":
        data = await reader.read(1024)
        file.write(data)

        writer.write(data)
        await writer.drain()
    file.close()
    writer.close()
    await writer.wait_closed()

async def send_file(reader, writer):


    
    print("lets print")
    name_file = input()
    print("Гарна назва файлу ", name_file)
    file = open(name_file, 'rb')
    print("знайшов цей файл", file)
    writer.write(name_file.encode())
    await writer.drain()
    print("Відправив назву")

    while True:
        line = file.read(1024)
        if not line:
            break
        print("Рядок віршу ", line)
        writer.write(line)
        print ("Ти диви, ще рядок", line)
        await writer.drain()
        
        print("Рядок віршу", line)

        
    writer.write(b"end")
    await writer.drain()


async def main():
    print("main")
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("connect")
    send = send_file(reader, writer)
    client = run_cliend(reader, writer)
    

    asyncio.create_task(send)
    await client
        

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

