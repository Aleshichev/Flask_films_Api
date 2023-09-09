"""
Results 10 films :
PopulateDB ------------ Done in 14.42 sec
PopulateDBThreaded ---- Done in 4.32 sec.
ThreadPoolExecutor ---- Done in 4.46 sec.
ProcessPoolExecutor --- Done in 8.48 sec.

Results 100 films :
PopulateDB ------------ Done in 139.63 sec.
PopulateDBThreaded ---- Done in 17.49 sec.
ThreadPoolExecutor ---- Done in 21.35 sec.
ProcessPoolExecutor --- Done in 36.87 sec.

"""
import datetime
from src.services.film_service import FilmService
import bs4
import requests
from src import db
from flask_restful import Resource
import re
import threading
# from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor


def check_release_date(release_date):

    if len(release_date) == 4:
        new_date = '01 January ' + release_date
        release_date = datetime.datetime.strptime(new_date.strip(), '%d %B %Y')
    else:
        release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')

    return release_date


def remove_leading_alpha_or_zero(input_string):
    # Use a regular expression to remove leading alphabetic characters or '0'
    result = re.sub(r'^[a-zA-Z0]*', '', input_string)
    return result

def convert_time(time: str) -> float:
    hour, minute = time.split('h')
    minutes = (60 * int(hour)) + int(minute.strip('min'))
    return minutes


def check_length(length):
    if type(length[:1]) == str:
        length = remove_leading_alpha_or_zero(length)
    if length[:1] == 0:
        length = remove_leading_alpha_or_zero(length)
    if length[-1:] == 'h':
        length = length[-2:] + ' 5m'

    new_length = float(convert_time(length))
    return new_length


class PopulateDB(Resource):

    def __init__(self, headers=None):
        super().__init__()
        self.url = 'https://www.imdb.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def get(self):
        t0 = datetime.datetime.now()
        print(t0)
        films_urls = self.get_films_urls()
        films = self.parse_films(films_urls)
        created_films = self.populate_db_with_films(films)
        dt = datetime.datetime.now() - t0
        print(f'Done in {dt.total_seconds():.2f} sec.')
        return {'message': f'Database were populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting films urls', flush=True)
        url = self.url + 'chart/top'
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:1]
        return movie_links

    def parse_films(self, film_urls):
        films_to_create = []
        for url in film_urls:
            url = self.url + url
            film_content = requests.get(url, headers=self.headers)
            film_content.raise_for_status()

            html = film_content.text
            soup = bs4.BeautifulSoup(html, features="html.parser")
            title = soup.find('span', class_='sc-afe43def-1 fDTGTb').text.split('(')[0].strip("[]'")
            rating = float(soup.find('span', class_='sc-bde20123-1 iZlgcd').text)
            description = soup.find('span', class_='sc-466bb6c-2 eVLpWt').text.strip()
            title_bar = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt').text
            release_date = title_bar[:4]
            release_date = check_release_date(release_date)

            length = title_bar[-6:]
            length = check_length(length)

            films_to_create.append(
                {
                    'title': title,
                    'rating': rating,
                    'description': description,
                    'release_date': release_date,
                    'length': length,
                    'distributed_by': 'Warner Bros. Pictures',
                }
            )
        return films_to_create

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)


class PopulateDBThreaded(Resource):
    def __init__(self, headers=None):
        super().__init__()
        self.url = 'https://www.imdb.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def get(self):
        threads = []
        films_to_create = []
        t0 = datetime.datetime.now()
        film_urls = self.get_film_urls()
        for film_url in film_urls:
            threads.append(threading.Thread(target=self.parse_films, args=(film_url, films_to_create), daemon=True))
        [t.start() for t in threads]
        [t.join() for t in threads]
        created_films = self.populate_db_with_films(films_to_create)

        dt = datetime.datetime.now() - t0
        print(f"Done in {dt.total_seconds():.2f} sec.")

        return {'message': f'Database were populated with {created_films} films.'}, 201

    def get_film_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top/'
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        html = resp.text
        soup = bs4.BeautifulSoup(html, features="html.parser")
        movie_containers = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:1]
        return movie_links

    def parse_films(self, film_url, films_to_create):
        url = self.url + film_url
        print(f'Getting a detailed info about the film - {url}')
        film_content = requests.get(url, headers=self.headers)
        film_content.raise_for_status()

        html = film_content.text
        soup = bs4.BeautifulSoup(html, features="html.parser")
        title = soup.find('span', class_='sc-afe43def-1 fDTGTb').text.split('(')[0].strip("[]'")
        rating = float(soup.find('span', class_='sc-bde20123-1 iZlgcd').text)
        description = soup.find('span', class_='sc-466bb6c-2 eVLpWt').text.strip()
        title_bar = soup.find('ul',
                              class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt').text
        release_date = title_bar[:4]
        release_date = check_release_date(release_date)


        length = title_bar[-6:]
        length = check_length(length)

        films_to_create.append(
            {
                'title': title,
                'rating': rating,
                'description': description,
                'release_date': release_date,
                'length': length,
                'distributed_by': 'Warner Bros. Pictures',
            }
        )
        return films_to_create


    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)


class PopulateDBThreadPoolExecutor(Resource):
    def __init__(self, headers=None):
        super().__init__()
        self.url = 'https://www.imdb.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def get(self):
        t0 = datetime.datetime.now()
        film_urls = self.get_film_urls()
        work = []
        with PoolExecutor() as executor:
            for film_url in film_urls:
                f = executor.submit(self.parse_films, film_url)
                work.append(f)
        films_to_create = [f.result() for f in work]
        created_films = self.populate_db_with_films(films_to_create)

        dt = datetime.datetime.now() - t0
        print(f"Done in {dt.total_seconds():.2f} sec.")

        return {'message': f'Database were populated with {created_films} films.'}, 201

    def get_film_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top/'
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        html = resp.text
        soup = bs4.BeautifulSoup(html, features="html.parser")
        movie_containers = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:1]

        return movie_links

    def parse_films(self, film_url):
        url = self.url + film_url
        print(f'Getting a detailed info about the film - {url}', flush=True)
        film_content = requests.get(url, headers=self.headers)
        film_content.raise_for_status()

        html = film_content.text
        soup = bs4.BeautifulSoup(html, features="html.parser")
        title = soup.find('span', class_='sc-afe43def-1 fDTGTb').text.split('(')[0].strip("[]'")
        rating = float(soup.find('span', class_='sc-bde20123-1 iZlgcd').text)
        description = soup.find('span', class_='sc-466bb6c-2 eVLpWt').text.strip()
        title_bar = soup.find('ul',
                              class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt').text
        release_date = title_bar[:4]
        release_date = check_release_date(release_date)

        length = title_bar[-6:]
        length = check_length(length)

        print(f'Received information about - {title}', flush=True)
        return {
            'title': title,
            'rating': rating,
            'description': description,
            'release_date': release_date,
            'length': length,
            'distributed_by': 'Warner Bros. Pictures',
        }

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)
