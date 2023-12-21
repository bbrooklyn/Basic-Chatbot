# The 5 W questions and how - who, what, when, where, why, how
from dynamic_responses import *
from collections import Counter

questions = {
    "who": {
        "responses": {
            "created you": Response(
                "I was created by Brooklyn Limbert, a student at Liverpool Hope University"
            ),
            "made you": Response(
                "I was made by Brooklyn Limbert, a student at Liverpool Hope University"
            ),
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
            "is your favourite subject": Response(
                "My favourite subject is Computer Science"
            ),
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
    "hello": "Hi, I'm a chatbot!",
    "my": {
        "responses": {
            "name is": Response("Nice to meet you!"),
        }
    },
    "tell": {
        "responses": {
            "me a joke": JokeResponse(),
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
            # A prompt is a message the user can send to the chatbot, triggering a response
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
                    Warning("Response is not a Response object, this may cause errors")
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


class Message:
    def __init__(self, message_body):
        self.raw_message = str(message_body)


class SpellChecker:
    def __init__(self, word, words, lexemes):
        # turn words dict into a list
        self.word = word
        self.words = Counter(list(words.keys()))
        self.lexemes = lexemes

    def correction(self):
        word = self.word
        word = word.lower()
        word = word.strip()
        correction = None
        for possible_word in self.words:
            print(possible_word)
            for i in range(len(word)):
                print("Word:", word)
                if word == possible_word or possible_word.startswith(word):
                    print("Word prev:", word)
                    correction = possible_word
                    break
                else:
                    word = word[:-1]
                    if len(word) == 0:
                        break
        return correction


class MessageInterpreter:
    def __init__(self):
        """
        Message parser class to interepret the message and return a response
        """
        self.responses = ResponseParser()
        self.responses.parse()  # Parse the responses into a lexicon tree
        self.last_prompt = None
        self.follow_up = False

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
        try:
            self.follow_up = False
            if self.last_prompt:
                print("Last prompt:", self.last_prompt)
                if self.last_prompt.follow_up:
                    print("Follow up:", self.last_prompt.follow_up)
                    self.follow_up = True
                    return self.last_prompt
            response = None
            lexicon_tree = self.responses.get_lexicon_tree()
            lexemes = self.get_lexemes(message)
            lexeme_index = 0
            current_branch = lexicon_tree
            parent_branch = lexicon_tree
            while response is None and lexeme_index < len(lexemes):
                lexeme = lexemes[lexeme_index]
                # check if there is a response or action
                current_branch = current_branch.get(lexeme, {})
                # NO RESPONSE FOUND, CHECK IF THERE IS A SIMILAR LEXEME
                if current_branch == {}:
                    spellchecker = SpellChecker(lexeme, parent_branch, lexemes)
                    correction = spellchecker.correction()
                    if correction:
                        current_branch = parent_branch[correction]
                    else:
                        possible_words = list(parent_branch.keys())
                        return Response(
                            f"I'm not sure how to respond to that.\nThe word ({lexeme}) was unexpected, did you mean: "
                            + ", ".join(possible_words[:-1])
                            + " or "
                            + possible_words[-1]
                            + "?"
                        )

                # RESPONSE FOUND, RETURN RESPONSE
                if "[response]" in current_branch:
                    response = current_branch["[response]"]
                    break
                lexeme_index += 1
                parent_branch = current_branch
            self.last_prompt = response
            if not response:
                return Response("I'm not sure how to respond to that")
            return response
        except Exception as e:
            print(e)
            return Response("Sorry, there was an error, I'm not sure how to respond.")

    def is_follow_up(self):
        return self.follow_up
