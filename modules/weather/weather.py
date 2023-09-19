import requests


async def get_weather(city:str):

    key = "cdd4546e3484a6afbdd4fbb028fa628d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    result = requests.get(url)
    weather = result.json()

    info = {
        'name': weather['name'],
        'temp': weather['main']['temp'],
        'feels_like': weather['main']['feels_like']
    }

    return info
