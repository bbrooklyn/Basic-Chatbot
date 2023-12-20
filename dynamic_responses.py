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


class WeatherResponse(Response):
    def __init__(self, response_body=None):
        super().__init__(response_body)
        # Override the follow_up attribute
        self.follow_up = True

    def get_response(self):
        return self.response_body
