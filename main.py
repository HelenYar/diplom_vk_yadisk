from vk import YandexDisk

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


if __name__ == '__main__':
    ya = YandexDisk(token_ya)
    ya.upload_yad(token_ya)
