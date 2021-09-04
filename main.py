import json
import os

import requests

from yandex_api import YaUploader


def get_profile_photos(owner_id, token):
    params = {
        'owner_id': owner_id,
        'access_token': token,
        'album_id': 'profile',
        'v': '5.77',
        'photo_sizes': '1',
        'extended': '1'
    }
    url = 'https://api.vk.com/method/photos.get'
    response = requests.get(
        url=url,
        params=params
    )
    if response.status_code == 200:
        json_output = response.json()
        json_file_data = []
        for item in json_output['response']['items']:
            item_with_max_size = get_max_size(*item['sizes'])
            likes = item['likes']['count']
            date = item['date']

            file_name = download_photo(
                url=item_with_max_size['url'],
                likes=likes,
                date=date
            )
            size = str(item_with_max_size['width']) + 'x' + str(item_with_max_size['height'])
            json_file_data.append(
                {
                    'file_name': file_name,
                    'size': size
                }
            )
        with open('photos.json', 'w') as file:
            file.write(json.dumps(json_file_data))
    else:
        print(response.status_code)


def download_photo(url, likes, date):
    response = requests.get(url=url)
    if response.status_code == 200:
        directory = 'photos'
        file_type = response.headers['Content-Type'].split('/')[1]
        print(file_type)
        file_name = directory + '/' + str(likes) + '.' + file_type
        if os.path.exists(file_name):
            file_name = directory + '/' + str(likes) + str(date) + '.' + file_type
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return file_name.split('/')[-1]


def get_max_size(*sizes):
    sizes_sorted = sorted(sizes, key=lambda item: item['height'])
    print(sizes_sorted)
    return sizes_sorted[-1]


def upload_to_yd(token, file_path):
    uploader = YaUploader(token)
    print('Загружаю файл: ', file_path)
    result = uploader.upload(file_path)


if __name__ == '__main__':
    owner_id = input('Введите id пользователя VK: ')
    ya_token = input('Введите токен Яндекса: ')
    get_profile_photos(
        owner_id=owner_id,
        token='958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    )
    file_list = os.listdir('photos')
    for file in file_list:
        upload_to_yd(ya_token, 'photos/' + file)
