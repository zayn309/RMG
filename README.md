# RMG — Random Movie Generator

Can't decide what to watch? **RMG** picks a random film from your **Letterboxd** watchlist (or any of your Letterboxd lists) and shows it in a desktop app styled like Letterboxd.

## Features

- Enter a Letterboxd username, and optionally a list name, to load your films.
- Scrapes every page of the watchlist or list with `requests` and BeautifulSoup.
- Picks a random film and shows its **poster, title, release year, rating, top cast, and description**.
- Fetches film pages and posters asynchronously with `aiohttp`, so the UI stays responsive.
- Quick links to open the film in your browser.
- Custom Pygame GUI built with `pygame_gui` and custom fonts and buttons.

## Getting started

```bash
pip install -r requirements.txt
python main.py
```

`CairoSVG` needs the Cairo library installed on your system to render the SVG logos.

## Tech stack

Python · Pygame (pygame-ce) · pygame_gui · BeautifulSoup · aiohttp · requests · CairoSVG

## License

[MIT](LICENSE)
