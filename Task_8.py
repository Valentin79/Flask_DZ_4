# Напишите программу, которая будет скачивать страницы из
# списка URL-адресов и сохранять их в отдельные файлы на
# диске.
# В списке может быть несколько сотен URL-адресов.
# При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# Представьте три варианта решения.
import requests
import threading
import multiprocessing
from datetime import datetime, time
import asyncio
import aiohttp

# urls = ['https://www.google.ru/',
#         'https://gb.ru/',
#         'https://ya.ru/',
#         'https://habr.com/ru/all/',
#         ]
urls = ["https://gosuslugi.ru/",
        "https://yandex.ru/",
        "https://youtube.com/",
        "https://google.com/",
        "https://vk.com/",
        "https://market.yandex.ru/",
        "https://music.yandex.ru/",
        "https://drive2.ru/",
        "https://sports.ru/",
        "https://2gis.ru/",
        ]


def parser_url(url):
    response = requests.get(url)
    filename = url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(f"files/{filename}", "w", encoding='utf-8') as f:
        f.write(response.text)


def threading_test(urls):
    dt = datetime.now()
    threads = []
    for url in urls:
        t = threading.Thread(target=parser_url, args=(url,))
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
        p = multiprocessing.Process(target=parser_url, args=(url,))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(f"Мультипроцессоринг зваершен за {datetime.now() - dt} секунд")


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            with open(f"files/{filename}", "w", encoding='utf-8') as f:
                f.write(text)


async def asyncio_test(urls):
    dt = datetime.now()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Асинхронная загрузка зваершена за {datetime.now() - dt} секунд")


if __name__ == '__main__':
    threading_test(urls)
    multiprocessing_test(urls)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio_test(urls))
