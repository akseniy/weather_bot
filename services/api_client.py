import requests


def test_city(admin_token, city):
    url = "http://api.weatherapi.com/v1/current.json?" + f'key={admin_token}&' f'q={city}'
    response = requests.get(url)  # Выполнение запроса с помощью метода `get()`
    json_data = response.json()  # Преобразование ответа в JSON с помощью метода `json()`
    code = response.status_code
    return code, json_data


def weather(admin_token, city):
    url = "http://api.weatherapi.com/v1/current.json?" + f'key={admin_token}&' f'q={city}'
    response = requests.get(url)  # Выполнение запроса с помощью метода `get()`
    json_data = response.json()  # Преобразование ответа в JSON с помощью метода `json()`
    code = response.status_code
    return code, json_data


def forecast(admin_token, city):
    url = "http://api.weatherapi.com/v1/forecast.json?" + f'key={admin_token}&' f'q={city}&days=3'
    response = requests.get(url)  # Выполнение запроса с помощью метода `get()`
    json_data = response.json()  # Преобразование ответа в JSON с помощью метода `json()`
    code = response.status_code
    return code, json_data
