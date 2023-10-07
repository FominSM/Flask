import threading, multiprocessing, asyncio
import requests, aiohttp
import argparse, sys, time


_thread_running_time = 0
_multiprocessing_running_time = multiprocessing.Value('d', 0.0)
_asyncio_time = 0


def _worker_threads(img_url, time_start, mode='multiprocessor', multiprocessing_time=None):
    '''Multi-threaded image downloading'''
  
    file_name = 'thread_' + img_url.split('/')[-1]

    response = requests.get(img_url)
    with open(f'img/{file_name}', 'wb') as f:
        f.write(response.content)

    global _thread_running_time
    time_work = time.time() - time_start
    _thread_running_time += round(time_work, 3)
    print(f'{round(time_work, 3)} img url - {img_url} ')
    

def _worker_process(img_url, time_start, multiprocessing_time):
    '''Multi-process image downloading'''

    file_name = 'process_' + img_url.split('/')[-1]

    response = requests.get(img_url)
    with open(f'img/{file_name}', 'wb') as f:
        f.write(response.content)

    time_work = time.time() - time_start
    with multiprocessing_time.get_lock():
        multiprocessing_time.value += round(time_work, 3)
    print(f'{round(time_work, 3)} img url - {img_url} ')


def multithreaded_and_multithreaded_downloads_images(mode='multiprocessor'):
    '''Thread and Process management'''

    process_or_thread_storage = []

    if mode == 'multithreaded':
        for url in urls:
            thread = threading.Thread(target=_worker_threads, args=(url, time.time(), 'multithreaded',))    
            process_or_thread_storage.append(thread)    
            thread.start()
    else:
        for url in urls:
            process = multiprocessing.Process(target=_worker_process, args=(url, time.time(), _multiprocessing_running_time, ))    
            process_or_thread_storage.append(process)    
            process.start()
           
    for task in process_or_thread_storage:    
        task.join()


async def process_file(url):
    global _asyncio_time
    global start_as_time

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            file_name = 'async' + url.split('/')[-1]

            with open(f'img/{file_name}', 'wb') as f:
                f.write(content)
            print(f'{time.time() - start_as_time} img url - {url} ')
            _asyncio_time += (time.time() - start_as_time)


async def main(urls):
    '''Manager asyncio'''

    tasks = []
    for url in urls:
        task = asyncio.ensure_future(process_file(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


def __urls_parser_from_file(file_name) -> list:
    '''Reads url-addresses and writes them to a list'''

    urls_list = []
    try:
        with open(f'url_paths_to_img/{file_name}', 'r', encoding='utf-8') as f:
            for line in f:
                urls_list.append(line[:-1])
            return urls_list
    except Exception as e:
        print(e)
        return None



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', '--name', default='default_path.txt')
    namespace = parser.parse_args(sys.argv[1:])

    urls = __urls_parser_from_file(namespace.name)

    print('\n\tThreads started')
    multithreaded_and_multithreaded_downloads_images('multithreaded')
    print(f'\tTotal running time of threads - {_thread_running_time}')

    print('\n\tProcesses started')
    multithreaded_and_multithreaded_downloads_images()
    print(f'\tTotal running time of processes - {_multiprocessing_running_time.value}')

    print('\n\tAsync started')
    start_as_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    print(f'\tTotal running time of async - {_asyncio_time}')

    

