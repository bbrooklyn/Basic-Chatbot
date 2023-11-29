import customtkinter
import requests
import random
# 01 Adjust chatbot responses based on weather, time of day, or other factors.

class App(customtkinter.CTk):
    def __init__(self, joke_sample_size=10):
        super().__init__()
        
        self.JOKE_SAMPLE_SIZE = joke_sample_size # How many jokes to fetch from the API
        
        self.responses = {
            "hello": "Hello, how are you?",
            "how are you?": "I'm good, thanks for asking!",#01FLAG
            "what is your name?": "My name is Chatbot",
            "who created you?": "I was created by Brooklyn Limbert, a student at Liverpool Hope University",
            "tell me a joke": self.__tell_joke,
        }
        # Pre-fetched calls
        self.jokes = self.fetch_jokes()
        
        # App configurations
        self.geometry("600x500")
        self.minsize(600, 500)
        self.title("Chatbot")

        # Grid configurations to position elements on the gui
        self.grid_columnconfigure(0, weight=1)  # Configure column
        self.grid_rowconfigure(1, weight=1)  # Configure row

        # Title of the app
        self.title = customtkinter.CTkLabel(
            self, text="Hello, I'm a chatbot!", text_color="black", height=3)
        self.title.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Entry for the user to enter their message to the chatbot
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter your message here")
        # Positioned bottom centre
        self.entry.grid(row=1, column=0, padx=5, pady=10, sticky="sew")
        # Positioned bottom right
        self.send_message_button = customtkinter.CTkButton(
            self, text="Send message", command=self.send_message)
        self.send_message_button.grid(
            row=1, column=1, pady=10, sticky="sew")
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self, width=200, height=380)
        self.scrollable_frame.grid(
            row=1, column=0, columnspan=2, pady=5, sticky="new")
        
    # Pre Fetching
    # These functions are called before the app is loaded        
    def fetch_jokes(self):
        # Fetch jokes from the API
        try:
            jokes = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&amount="+str(self.JOKE_SAMPLE_SIZE)).json()
            print(jokes)
            return jokes.get("jokes")
        except Exception as e:
            print(e)
            return None
        
    # Custom responses
    # These are chatbot responses that are not pre-defined
    def __tell_joke(self):
        # Tell a joke
        if self.jokes is not None:
            joke = self.jokes.pop()
            return joke.get("setup") + "\n...\n" + joke.get("delivery")
        else:
            return "Sorry, I couldn't fetch any jokes"
            
    # Sending & getting messages    
    # These functions are called when the user sends a message
    def get_response(self, message):
        response = self.responses.get(message, "I'm not sure how to respond to that.")
        
        # Call function fetched from dictionary
        if callable(response):
            print("Calling function")
            return response()
        else:
            return response
    
    def __dumify_message(self, message):
        # Remove punctuation
        message = message.strip()
        message = message.lower()
        return message

    def send_message(self):
        # Get the message from the entry
        message = self.entry.get()
        message = self.__dumify_message(message)

        if message != "":
            print(message)

            self.new_bubble(message, is_user=True)
            response = self.get_response(message)
            
            self.new_bubble(response, is_user=False) # Send response
            self.entry.delete(0, 'end') # Clear the entry
        
    # Chat bubbles & graphics
    # These functions are used to display graphics on the application
    def new_bubble(self, message, is_user=False):
        # Create bubble chat
        if is_user:
            MSG_COLOR = "#2eb4ea"
            AUTHOR_COLOR = "#1c6c8c"
            AUTHOR = "You"
        else:
            MSG_COLOR = "#2ecc48"
            AUTHOR_COLOR = "#28b33f"
            AUTHOR = "Chatbot"

        message_frame = customtkinter.CTkFrame(
            self.scrollable_frame)
        message_frame.grid_rowconfigure(0, weight=1)
        message_frame.grid_columnconfigure(0, weight=1)
        author = customtkinter.CTkLabel(
            message_frame, text=AUTHOR, text_color="white", fg_color=AUTHOR_COLOR, corner_radius=10, width=60)
        author.grid(padx=10, row=0, column=0)
        message = customtkinter.CTkLabel(message_frame, text=message, text_color="white",
                                         fg_color=MSG_COLOR, justify="left", corner_radius=10, wraplength=400)
        message.grid(row=0, column=1)
        message_frame.grid(padx=5, pady=5, sticky="w")

app = App(
    joke_sample_size=15
    
)
app.mainloop()
