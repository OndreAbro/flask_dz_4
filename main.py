import sys
import time
import requests
import threading
import multiprocessing
import asyncio


def download_image(url):
    filename = url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")


async def async_download_image(url):
    filename = url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")


def main_threading(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=download_image, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"Total time with threading: {end_time - start_time} seconds")


def main_multiprocessing(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_image, args=(url,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    print(f"Total time with multiprocessing: {end_time - start_time} seconds")


async def main_asyncio(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        tasks.append(async_download_image(url))
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Total time with asyncio: {end_time - start_time} seconds")


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python download_images.py <url1> <url2> ...")
        sys.exit(1)

    main_threading(urls)
    main_multiprocessing(urls)
    asyncio.run(main_asyncio(urls))