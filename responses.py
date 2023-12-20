# The 5 W questions and how - who, what, when, where, why, how
from dynamic_responses import *

questions = {
    "who": {
        "responses": {
            "created you": Response("I was created by Brooklyn Limbert, a student at Liverpool Hope University"),
            "are you": Response("I'm Chatbot, a chatbot created by Brooklyn Limbert"),
        }
    },
    "what": {
        "responses": {
            "is your name": Response("My name is chatterbot"),
            "is your favourite colour": Response("My favourite colour is blue"),
            "is your favourite food": Response("My favourite food is pizza"),
            "is your favourite animal": Response("My favourite animal is a dog"),
            "is your favourite sport": Response("My favourite sport is football"),
            "is your favourite subject": Response("My favourite subject is Computer Science"),
            "is your favourite book": Response("My favourite book is Harry Potter"),
            "is your favourite film": Response("My favourite film is The Dark Knight"),
            "is your favourite tv show": Response("My favourite tv show is The Office"),
            "is the weather like": WeatherResponse(),
        }
    },
    "when": {
        "responses": {
            "is your birthday": Response("My birthday is 1st January 2021"),
        }
    },
    "where": {
        "responses": {
            "do you live": Response("I live in Liverpool, England"),
        }
    },
    "how": {
        "responses": {
            "are you": Response("I'm good, thanks for asking!"),
        }
    },
}

statements = {
    "hello": "",
    "my": {
        "responses": {
            "name is": Response("Nice to meet you!"),
        }
    },
}


class ResponseParser:
    def __init__(self):
        """
        Response parser class to parse the responses into a lexicon tree
        """
        self.questions = questions
        self.statements = statements
        self.__lexicon_tree = {}

    def get_lexicon_tree(self):
        return self.__lexicon_tree

    def parse(self):
        """
        Parse the responses into a lexicon tree
        """
        # Add the questions to the lexicon tree
        for lexeme, data in questions.items():
            if lexeme not in self.__lexicon_tree:
                self.__lexicon_tree[lexeme] = {}

            # Add the responses to the lexicon tree
            # A trigger is a message the user can send to the chatbot, triggering a response
            for prompt_message, response in data["responses"].items():
                prompt_lexemes = prompt_message.split(" ")
                current_lexicon_tree = self.__lexicon_tree[lexeme]
                lexeme_index = 0

                while lexeme_index < len(prompt_lexemes):
                    prompt_lexeme = prompt_lexemes[lexeme_index]

                    if prompt_lexeme not in current_lexicon_tree:
                        current_lexicon_tree[prompt_lexeme] = {}

                    current_lexicon_tree = current_lexicon_tree[prompt_lexeme]
                    lexeme_index += 1
                current_lexicon_tree["[response]"] = response

        # Add the statements to the lexicon tree
        for lexeme, data in statements.items():
            if lexeme not in self.__lexicon_tree:
                self.__lexicon_tree[lexeme] = {}

            # Add the responses to the lexicon tree
            if type(data) != dict:
                if type(data) != Response:
                    Warning(
                        "Response is not a Response object, this may cause errors")
                    self.__lexicon_tree[lexeme]["[response]"] = Response(data)
                else:
                    self.__lexicon_tree[lexeme]["[response]"] = data
                continue

            for prompt_message, response in data["responses"].items():
                prompt_lexemes = prompt_message.split(" ")

                current_lexicon_tree = self.__lexicon_tree[lexeme]
                lexeme_index = 0

                while lexeme_index < len(prompt_lexemes):
                    prompt_lexeme = prompt_lexemes[lexeme_index]

                    if prompt_lexeme not in current_lexicon_tree:
                        current_lexicon_tree[prompt_lexeme] = {}

                    current_lexicon_tree = current_lexicon_tree[prompt_lexeme]
                    lexeme_index += 1
                current_lexicon_tree["[response]"] = response


class Message():
    def __init__(self, message_body):
        self.raw_message = str(message_body)


class MessageInterpreter:
    def __init__(self):
        """
        Message parser class to interepret the message and return a response
        """
        self.responses = ResponseParser()
        self.responses.parse()  # Parse the responses into a lexicon tree

    def get_lexemes(self, message: Message):
        raw_message = message.raw_message

        punctuation = [".", ",", "?", "!", "'"]
        for char in punctuation:
            raw_message = raw_message.replace(char, "")
        raw_message = raw_message.lower()
        raw_message.strip()

        lexemes = raw_message.split(" ")
        return lexemes

    def interpret(self, message: Message):

        lexemes = self.get_lexemes(message)
        lexicon_tree = self.responses.get_lexicon_tree()

        response = None
        print(lexemes)
        lexeme_index = 0
        current_branch = lexicon_tree

        while response is None:
            lexeme = lexemes[lexeme_index]
            # check if there is a response or action

            current_branch = current_branch.get(lexeme)

            if current_branch is None:  # No branch, invalid message or no response available
                # Todo: find similar lexemes
                print("No branch")

            if "[response]" in current_branch:
                response = current_branch["[response]"]
                break
            else:
                print("No response")

            lexeme_index += 1

        print(response.get_response())

        return "END OF OUTPUT - MESSAGE INTERPRETER"


message = Message("what is your favourite colour?")
m = MessageInterpreter()
print(m.interpret(message))
