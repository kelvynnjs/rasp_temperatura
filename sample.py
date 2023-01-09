import requests


def init():
    data = requests.get("http://192.168.1.5:5000").json()
    print(data)


if __name__ == '__main__':
    init()