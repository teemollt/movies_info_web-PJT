import requests

API_KEY = '3916e8dca704795c23c8ac7c915bfda6'
PAGE_NUM = 1

class URLMaker:
    url = 'https://api.themoviedb.org/3'

    def __init__(self, key):
        self.key = key

    def get_url(self, category='movie', feature='popular', **kwargs):
        url = f'{self.url}/{category}/{feature}'
        url += f'?api_key={self.key}'
        url += '&language=ko-KR'

        for k, v in kwargs.items():
            url += f'&{k}={v}'

        return url


    def movie_id(self, title):
        url = self.get_url('search', 'movie', region='KR', language='ko', query=title)
        res = requests.get(url)
        movie = res.json()

        if len(movie.get('results')):
            return movie.get('results')[0].get('id')
        else:
            return None

def get_movie_json():
    global PAGE_NUM
    url = URLMaker(API_KEY)
    raw_data = requests.get(url.get_url(page=PAGE_NUM))
    PAGE_NUM += 1
    json_data = raw_data.json()
    movie_data = json_data.get('results')

    return movie_data

genres = {
    '28': '액션',
    '12': '모험',
    '16': '애니메이션',
    '35': '코미디',
    '80': '범죄',
    '99': '다큐멘터리',
    '18': '드라마',
    '10751': '가족',
    '14': '판타지',
    '36': '역사',
    '27': '공포',
    '10402': '음악',
    '9648': '미스터리',
    '10749': '로맨스',
    '878': 'SF',
    '10770': 'TV 영화',
    '53': '스릴러',
    '10752': '전쟁',
    '37': '서부'
}