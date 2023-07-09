# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на
# диск. Каждое изображение должно сохраняться в отдельном файле,
# название которого соответствует названию изображения в URL-адресе.

import requests
import threading
import multiprocessing
from datetime import datetime, time
import asyncio
import aiohttp
import aiofiles

urls = [
    'https://gas-kvas.com/uploads/posts/2023-02/1675489216_gas-kvas-com-p-fonovii-risunok-leto-na-rabochii-stol-35.jpg',
    'https://wp-s.ru/wallpapers/0/12/471657930780807/morskie-kamni-raznocvetnaya-galka.jpg',
    'https://wp-s.ru/wallpapers/9/8/483395166098626/pejzazh-s-gorodom-na-fone-ozera-v-avstrii.jpg',
    'https://cdn.f1ne.ws/gallery/d/2035857-1/0001196502_1200px_0XSLJA00RZOSCC0Z17D4H08LZ8YU.jpg',
    'https://s.auto.drom.ru/i24283/pubs/4/94392/gen340_4120549.jpg'
]


def img_saver(url):
    response = requests.get(url).content
    filename = f'{url.split("/")[-1]}'
    with open(f'images/{filename}', 'wb') as f:
        f.write(response)


def threading_test(urls):
    dt = datetime.now()
    threads = []
    for url in urls:
        t = threading.Thread(target=img_saver, args=(url,))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Многопоточность зваершена за {datetime.now() - dt} секунд")


def multiprocessing_test(urls):
    dt = datetime.now()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=img_saver, args=(url,))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(f"Мультипроцессоринг зваершен за {datetime.now() - dt} секунд")


async def img_download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            filename = f'{url.split("/")[-1]}'
            img = await response.content.read()
            async with aiofiles.open(f'images/{filename}', "wb") as img_file:
                await img_file.write(img)


async def asyncio_test(urls):
    dt = datetime.now()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(img_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Асинхронная загрузка зваершена за {datetime.now() - dt} секунд")


if __name__ == '__main__':
    threading_test(urls)
    multiprocessing_test(urls)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio_test(urls))
