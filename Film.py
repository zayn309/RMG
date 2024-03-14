from bs4 import BeautifulSoup
from utils import main_domain
import json
import io
import pygame
import aiohttp
import asyncio

class Film:
    def __init__(self, container):
        self.filmslug = container.div["data-film-slug"]
        self.soup = None
        self.json = None
        self.movie_info = None

    async def get_film_page_async(self):
        url = main_domain + "film/" + self.filmslug + "/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                filmPage = await response.text()
                self.soup = BeautifulSoup(filmPage, "html.parser")

    def parse_jsone(self):
        script_tag = self.soup.find("script", type="application/ld+json")

        script_content = script_tag.string

        start_index = script_content.find("{")
        end_index = script_content.rfind("}") + 1

        json_content = script_content[start_index:end_index]

        self.json = json.loads(json_content)
        # with open("parsed_json.json", "w", encoding="utf-8") as json_file:
        #     json.dump(self.json, json_file, indent=4)

    async def get_poster_async(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.json["image"]) as response:
                    if response.status == 200:
                        image_bytes = await response.read()
                        image = pygame.image.load(io.BytesIO(image_bytes),"")
                        return image
                    else:
                        print("Failed to download the image. Status code:", response.status)
                        return None
        except Exception as e:
            print("Error downloading the image:", str(e))
            return None

    def get_film_name(self):
        return self.json["name"]

    def get_release_year(self):
        return self.json["releasedEvent"][0]["startDate"]

    def get_rating(self):
        rating_value = self.json["aggregateRating"]["ratingValue"]
        rating_count = self.json['aggregateRating']['ratingCount']
        rounded_rating = round(float(rating_value), 1)
        return (rounded_rating, rating_count)

    def get_actors(self):
        actors = self.json["actors"]
        top_actors = []
        for idx, actor in enumerate(actors):
            top_actors.append(actor["name"])
            if idx >= 4:
                break

        return top_actors

    def get_director(self):
        directors = []
        for director in self.json["director"]:
            directors.append(director["name"])
        return directors

    def get_genres(self):
        return self.json["genre"]

    def get_imdbLink(self):
        imdb_link = self.soup.find('a', {'data-track-action': 'IMDb'})['href']
        return imdb_link
    
    def get_ytsLink(self):
        link = 'https://yts.mx/movies/' + self.filmslug + '-' + str(self.get_release_year())
        return link

    def get_desc(self):
        return self.soup.find('meta', property="og:description")['content']
    

    async def save_movie_info_async(self):
        await self.get_film_page_async()

        self.parse_jsone()

        poster = await self.get_poster_async()
        self.movie_info = {
            "film_name": self.get_film_name(),
            "release_year": self.get_release_year(),
            "rating": self.get_rating(),
            "actors": self.get_actors(),
            "director": self.get_director(),
            "genres": self.get_genres(),
            "poster": poster,
            "imdb_link": self.get_imdbLink(),
            "yts_link": self.get_ytsLink(),
            'description': self.get_desc(),
        }

    def get_info(self):
        asyncio.run(self.save_movie_info_async())
        return self.movie_info

    def __hash__(self):
        return hash(self.filmslug)

    def __str__(self):
        disc = f"""
        name:{self.filmslug}
        """
        return disc
