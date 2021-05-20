import requests

API_KEY = '3916e8dca704795c23c8ac7c915bfda6'

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
    url = URLMaker(API_KEY)
    raw_data = requests.get(url.get_url(page=4))
    # print(raw_data)
    json_data = raw_data.json()
    movie_data = json_data.get('results')

    return movie_data

# {
#     "genres": [
#         {
#             "id": 28,
#             "name": "액션"
#         },
#         {
#             "id": 12,
#             "name": "모험"
#         },
#         {
#             "id": 16,
#             "name": "애니메이션"
#         },
#         {
#             "id": 35,
#             "name": "코미디"
#         },
#         {
#             "id": 80,
#             "name": "범죄"
#         },
#         {
#             "id": 99,
#             "name": "다큐멘터리"
#         },
#         {
#             "id": 18,
#             "name": "드라마"
#         },
#         {
#             "id": 10751,
#             "name": "가족"
#         },
#         {
#             "id": 14,
#             "name": "판타지"
#         },
#         {
#             "id": 36,
#             "name": "역사"
#         },
#         {
#             "id": 27,
#             "name": "공포"
#         },
#         {
#             "id": 10402,
#             "name": "음악"
#         },
#         {
#             "id": 9648,
#             "name": "미스터리"
#         },
#         {
#             "id": 10749,
#             "name": "로맨스"
#         },
#         {
#             "id": 878,
#             "name": "SF"
#         },
#         {
#             "id": 10770,
#             "name": "TV 영화"
#         },
#         {
#             "id": 53,
#             "name": "스릴러"
#         },
#         {
#             "id": 10752,
#             "name": "전쟁"
#         },
#         {
#             "id": 37,
#             "name": "서부"
#         }
#     ]
# }