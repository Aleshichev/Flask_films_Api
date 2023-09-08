import datetime
# from src.services.film_service import FilmService
import bs4
import requests
# from src import db
from flask_restful import Resource

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
    # url = 'https://www.imdb.com/'

    def get(self):
        t0 = datetime.datetime.now()
        print(t0)
        films_urls = self.get_films_urls()
        films = self.parse_films(films_urls)
        # created_films = self.populate_db_with_films()
        dt = datetime.datetime.now() - t0
        print(f'Done in {dt.total_seconds():.2f} sec.')
        # return  {'message': f'Database were populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting films urls', flush=True)
        url = self.url + 'chart/top'
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:2]
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
            # release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
            title_bar = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt').text
            release_date = title_bar[:4]
            length = title_bar[5:11]
        #     length = convert_time(soup.find('div', class_='subtext').time.text.strip())
        #     print(f'Received information about - {title}', flush=True)
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
            print(films_to_create)
        return films_to_create
    #
    # @staticmethod
    # def populate_db_with_films(films):
    #     return FilmService.bulk_create_films(db.session, films)








