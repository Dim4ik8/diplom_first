import requests
from urllib.parse import urlencode


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        print(self.token)

    def upload(self, file_path: str):

        url_for_prepare = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'

        upload_url = ''

        file_name = file_path.split('/')[-1]
        request_params = {'path': '/upload/' + file_name}

        params_encoded = urlencode(request_params)

        get_upload_url_request = requests.get(
            url=url_for_prepare + '?' + params_encoded,
            headers={'Authorization': self.token}
        )
        print("Код ответа первого запроса:" + str(get_upload_url_request.status_code))
        if get_upload_url_request.status_code == 200:
            response_data = get_upload_url_request.json()
            upload_url = response_data['href']
            print(upload_url)
        elif get_upload_url_request.status_code == 401:
            print('401 Вы не авторизованы')

        if upload_url != '':
            file_upload_request = requests.put(
                url=upload_url,
                data=open(file_path, 'rb'),
                headers={'Authorization': self.token}
            )
            if file_upload_request.status_code == 201:
                print('Файл успешно загружен.')
            elif file_upload_request.status_code == 507:
                print('Недостаточно места на диске!')
