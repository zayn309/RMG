
main_domain = "https://letterboxd.com/"

import threading
import requests
from bs4 import BeautifulSoup
import webbrowser
import asyncio
import aiohttp
import time
from Film import Film
import secrets
import cairosvg
import io
import pygame

def get_Films_list(username=None, listName="/watchlist/"):
    try:
        if listName != "/watchlist/":
            listName = "/list/" + listName + "/"

        url = main_domain + username + listName
        page_number = 1
        films = []

        while True:
            if page_number == 1:
                page_url = url
            else:
                page_url = url + "page/" + str(page_number) + "/"

            response = requests.get(page_url)
            response.raise_for_status()

            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            film_containers = soup.find_all(class_="poster-container")

            if not film_containers:
                break

            for container in film_containers:
                films.append(Film(container))

            page_number += 1

        return set(films)

    except requests.RequestException as e:
        print("Request Exception:", e)
        return None

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

def open_url_in_browser(url):
    """
    Opens the specified URL in the default web browser.
    
    Parameters:
        url (str): The URL to open in the browser.
        
    Returns:
        None
    """
    try:
        webbrowser.open(url)
    except FileNotFoundError:
        print("Failed to open the URL. Please make sure xdg-open is installed and try again.")


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_Films_list_async(username=None, listName="/watchlist/"):
    try:
        if listName != "/watchlist/":
            listName = "/list/" + listName + "/"
        
        url = main_domain + username + listName
        page_number = 1
        films = []

        async with aiohttp.ClientSession() as session:
            while True:
                if page_number == 1:
                    page_url = url
                else:
                    page_url = url + "page/" + str(page_number) + "/"
                
                html_content = await fetch_page(session, page_url)
                soup = BeautifulSoup(html_content, "html.parser")
                film_containers = soup.find_all(class_="poster-container")
                
                if not film_containers:
                    break

                for container in film_containers:
                    films.append(Film(container))
                
                page_number += 1
        
        return set(films)
    
    except aiohttp.ClientError as e:
        print("Request Exception:", e)
        return None

def get_random_film(username):
    list_ = asyncio.run(get_Films_list_async(username=username))
    rand_film = secrets.choice(list(list_))
    return rand_film

def url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def load_svg(filename):
    new_bites = cairosvg.svg2png(url = filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)



def kill_thread(thread_name):
    for thread in threading.enumerate():
        if thread.name == thread_name:
            thread.join()
            break

if __name__ == "__main__":
    start_time_async = time.time()
    list_ = asyncio.run(get_Films_list_async(username="Z_a_y_n"))
    end_time_async = time.time()
    async_duration = end_time_async - start_time_async
    for film in list_:
        print(film)

    start_time_sync = time.time()
    list_ = get_Films_list(username="jay")
    end_time_sync = time.time()
    sync_duration = end_time_sync - start_time_sync
    print("Async Function Duration:", async_duration)
    print("Sync Function Duration:", sync_duration)


