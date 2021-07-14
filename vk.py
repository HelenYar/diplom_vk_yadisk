import requests
import datetime
import json
import time
from tqdm import tqdm

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


class Vk:

    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {'access_token': token, 'v': '5.131'}
    # user_id 148916467

    def get_photos(self):
        user_id = input("Введите user_id: ")
        count = input("Введите количество фотографий для копирования: ")
        get_photo_url = self.url + 'photos.get'
        get_photo_params = {'user_id': user_id, 'extended': '1',
                            'album_id': 'profile', 'count': count, 'photo_sizes': '1'}
        req = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()
        return req['response']['items']


    def get_name_file(self):
        l_photos = []
        list_photos = []
        like = []
        photos = self.get_photos()
        for photo in photos:
            p_data = (datetime.datetime.fromtimestamp(photo['date'])).strftime('%d-%m-%Y')
            p_likes = photo['likes']['count']
            p_url = photo['sizes'][len(photo['sizes'])-1]['url']
            p_size = photo['sizes'][len(photo['sizes'])-1]['type']
            if p_likes not in like:
                l_photos.append({'Name': str(p_likes)+'.jpg', 'Likes': str(p_likes), 'Date': p_data, 'Url': p_url, 'Size type': p_size})
                list_photos.append({"file_name": str(p_likes) + '.jpg', "size": p_size})
            else:
                l_photos.append({'Name': str(p_likes) + "_" + p_data+'.jpg', 'Likes': str(p_likes), 'Date': p_data, 'Url': p_url, 'Size type': p_size})
                list_photos.append({"file_name": str(p_likes) + "_" + p_data+'.jpg', "size": p_size})
            like.append(p_likes)

            with open('photos.json', 'w') as f:
                json.dump(list_photos, f, indent=2, ensure_ascii=False)
        print(l_photos)
        return l_photos


class YandexDisk:
    with open('token_ya.txt', 'r') as file_object:
        token_ya = file_object.read().strip()

    def __init__(self, token_ya):
        self.token_ya = token_ya

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token_ya)}

    def papka(self, token_ya):
        url_ya_p = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': 'OAuth ' + token_ya}
        requests.put(url_ya_p, headers=headers, params={'path': "/vk_photos"})

    def upload_yad(self, token_ya):
        self.papka(token_ya)
        url_yad = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': 'OAuth ' + token_ya}
        name_list = []
        vk = Vk(token)
        vk_list = vk.get_name_file()
        for photo in vk_list:
            name = str(photo['Name'])
            name_list.append(name)
            requests.post(url_yad, headers=headers, params={'url': photo['Url'], 'path': "/vk_photos/" + name})
            for i in tqdm(range(1)):
                time.sleep(1)