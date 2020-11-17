import requests
import json
import re
import os


def build_imdb_SearchMovie_request(language, api_key, title):
    url = '/'.join(['https://imdb-api.com', language, 'API/SearchMovie', api_key, title])
    print('looking for ' + title + '...')
    return url


def imdb_SearchMovie(url, headers, payload):
    response = requests.request('GET', url, headers=headers, data=payload)
    if response.status_code == 200:
        results = response.json()
        if results['results'] != 0:
            print('movie found!')
            return results
        else:
            print('ERROR: movie not found!')
            if len(results['errorMessage']) > 1:
                print(results['errorMessage'])
    else:
        print('someting went wrong...')
        print(response.status_code())


def extract_imdb_id(dataset):
    if dataset['results'][0]['id'] != 0:
        imdb_id = dataset['results'][0]['id']
        return imdb_id
    else:
        print('FAIL to extract imdb-id!')


def build_imdb_getTitle_request(language, api_key, imdb_id, options):
    url = "/".join(['https://imdb-api.com', language, 'API/Title', api_key, imdb_id, options])
    return url


def get_movie_data(url, headers, payload):
    print('get movie data...')
    response = requests.request('GET', url, headers=headers, data=payload)
    if response.status_code == 200:
        movie_data = response.json()
        return movie_data
    else:
        print('someting went wrong...')
        print(response.status_code())


def save_movie_data(dataset, path):
    title_raw = dataset['title']
    title = re.sub('[^a-zA-Z0-9 \n\.]', '', title_raw)
    print(title)
    year = dataset['year']
    print(year)
    filename = str(title + '_' + year + '.json')
    print(filename)
    filepath = path + filename
    with open(filepath, 'w') as movie_file:
        json.dump(dataset, movie_file, indent=4)
        print('data successfully saved.')


def get_movies_as_list(path):
    movies_as_list = []
    with open(path, 'r', encoding='utf-8') as data_file:
        movies_as_list = [line.rstrip() for line in data_file ]
    return movies_as_list


def count_saved_data(path):
    count = len(os.listdir(path))
    return count


language = 'en'
api_key = 'k_3rlgY00a'
headers = {}
payload = {}
options = ",".join(['FullActor', 'FullCast', 'Posters', 'Images', 'Trailer', 'Ratings', 'Wikipedia'])
path = './movie_data/'
movielist = get_movies_as_list('./input_data/movies.txt')

start = count_saved_data(path) + 1
end = start + 19

for i in range(start, end):
    print(i)
    title = movielist[i]
    search_url = build_imdb_SearchMovie_request(language, api_key, title)
    dataset = imdb_SearchMovie(search_url, headers, payload)
    imdb_id = extract_imdb_id(dataset)
    title_url = build_imdb_getTitle_request(language, api_key, imdb_id, options)
    movie_data = get_movie_data(title_url, headers, payload)
    save_movie_data(movie_data, path)

