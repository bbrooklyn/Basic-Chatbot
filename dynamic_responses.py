import random
import requests

class Response:

    def __init__(self, response_body=None):
        """
        response_body: The text that the chatbot will respond with
        """

        self.response_body = response_body
        self.follow_up = False

    def get_response(self) -> str:
        return self.response_body

#
class HowAreYouResponse(Response):
    def __init__(self, response_body=None):
        super().__init__(response_body)
        self.responses = ["I'm good, thanks for asking!", "I'm doing well, thanks for asking!", "I'm doing great, thanks for asking!"]

    def get_response(self):
        return random.choice(self.responses)
    
class JokeResponse(Response):
    def __init__(self, response_body=None):
        super().__init__(response_body)
        
    def get_response(self):
        joke_request = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        return joke_request.json()["joke"]

class WeatherResponse(Response):
    def __init__(self, response_body=None):
        super().__init__(response_body)
        # Override the follow_up attribute
        self.follow_up = True
        self.WEATHER_API_KEY = "a65a7dc955c742d890d33510232112"

    def get_response(self, location=None):
        if location:
            self.follow_up = False
            weather_request = requests.get(
                f"http://api.weatherapi.com/v1/current.json?key={self.WEATHER_API_KEY}&q={location}&aqi=no")
            weather_data = weather_request.json()
            print(weather_data)
            if weather_data.get("error"):
                self.follow_up = True
                return "I couldn't find that location, please try again"
            else:
                return f"The weather in {location} is {weather_data['current']['condition']['text']} and {weather_data['current']['temp_c']}°C"
        else:
            return "Where would you like to know the weather for?"
