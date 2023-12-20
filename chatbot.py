import customtkinter
import requests
from responses import MessageInterpreter
import random
# 01 Adjust chatbot responses based on weather, time of day, or other factors.


class App(customtkinter.CTk):
    def __init__(self, joke_sample_size=10):
        super().__init__()

        # How many jokes to fetch from the API
        self.JOKE_SAMPLE_SIZE = joke_sample_size

        self.message_interpreter = MessageInterpreter()
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

    def send_message(self):
        # Get the message from the entry
        message_text = self.entry.get()

        if message_text != "":
            message = Message(message_text)
            print(message)

            self.new_bubble(message, is_user=True)
            response = self.message_interpreter.interepret(message)

            self.new_bubble(response, is_user=False)  # Send response
            self.entry.delete(0, 'end')  # Clear the entry


class Message:
    def __init__(self, message_body=None):
        self.message_body = None

    def __str__(self):
        return self.message_body


app = App(
    joke_sample_size=15
)
app.mainloop()
