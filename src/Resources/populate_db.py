import datetime
from src.services.film_service import FilmService
import bs4
import requests
from src import db
from flask_restful import Resource
import threading
# from datetime import date
# from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor
# from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor


def convert_time(time: str) -> float:
    hour, minute = time.split('h')
    minutes = (60 * int(hour)) + int(minute.strip('min'))
    return minutes


class PopulateDB(Resource):

    def __init__(self, headers=None):
        super().__init__()  # Call the superclass constructor
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
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:10]
        return movie_links

    def parse_films(self, film_urls):
        films_to_create = []
        for url in film_urls:
            url = self.url + url
            print(f'Getting a detailed info about the film - {url}')
            film_content = requests.get(url, headers=self.headers)
            film_content.raise_for_status()

            html = film_content.text
            soup = bs4.BeautifulSoup(html, features="html.parser")
            title = soup.find('span', class_='sc-afe43def-1 fDTGTb').text.split('(')[0].strip("[]'")
            rating = float(soup.find('span', class_='sc-bde20123-1 iZlgcd').text)
            description = soup.find('span', class_='sc-466bb6c-2 eVLpWt').text.strip()
            # title_bar = soup.find('div', class_='titleBar').text.strip()
            # title_content = title_bar.split('\n')
            # release_date, _ = title_content[-1].split('(')
            title_bar = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt').text
            release_date = title_bar[:4]
            if len(release_date) == 4:
                new_date = ''
                new_date = '01 January ' + release_date
                # parts = [int(part.strip()) for part in release_date.split(',')]
                # date_tuple = tuple(parts)
                release_date = datetime.datetime.strptime(new_date.strip(), '%d %B %Y')
            else:
                release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
            length = float(convert_time(title_bar[-6:]))
            # length = convert_time(soup.find('div', class_='subtext').time.text.strip())
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
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:10]

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
        if len(release_date) == 4:
            # new_date = ''
            new_date = '01 January ' + release_date
            release_date = datetime.datetime.strptime(new_date.strip(), '%d %B %Y')
        else:
            release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
        length = float(convert_time(title_bar[-6:]))
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

#
# class PopulateDBThreadPoolExecutor(Resource):
#     url = 'https://www.imdb.com/'
#
#     def post(self):
#         t0 = datetime.datetime.now()
#         film_urls = self.get_film_urls()
#         work = []
#         with PoolExecutor() as executor:
#             for film_url in film_urls:
#                 f = executor.submit(self.parse_films, film_url)
#                 work.append(f)
#         films_to_create = [f.result() for f in work]
#         created_films = self.populate_db_with_films(films_to_create)
#
#         dt = datetime.datetime.now() - t0
#         print(f"Done in {dt.total_seconds():.2f} sec.")
#
#         return {'message': f'Database were populated with {created_films} films.'}, 201
#
#     def get_film_urls(self):
#         print('Getting film urls', flush=True)
#         url = self.url + 'chart/top/'
#         resp = requests.get(url)
#         resp.raise_for_status()
#
#         html = resp.text
#         soup = bs4.BeautifulSoup(html, features="html.parser")
#         movie_containers = soup.find_all('td', class_='posterColumn')
#         movie_links = [movie.a.attrs['href'] for movie in movie_containers][:11]
#
#         return movie_links
#
#     def parse_films(self, film_url):
#         url = self.url + film_url
#         print(f'Getting a detailed info about the film - {url}', flush=True)
#         film_content = requests.get(url)
#         film_content.raise_for_status()
#
#         html = film_content.text
#         soup = bs4.BeautifulSoup(html, features="html.parser")
#         title, _ = soup.find('div', class_='originalTitle').text.split('(')
#         rating = float(soup.find('div', class_='ratingValue').strong.text)
#         description = soup.find('div', class_='summary_text').text.strip()
#         title_bar = soup.find('div', class_='titleBar').text.strip()
#         title_content = title_bar.split('\n')
#         release_date, _ = title_content[-1].split('(')
#         release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
#         length = convert_time(soup.find('div', class_='subtext').time.text.strip())
#         print(f'Received information about - {title}', flush=True)
#         return {
#             'title': title,
#             'rating': rating,
#             'description': description,
#             'release_date': release_date,
#             'length': length,
#             'distributed_by': 'Warner Bros. Pictures',
#         }
#
#     @staticmethod
#     def populate_db_with_films(films):
#         return FilmService.bulk_create_films(db.session, films)
