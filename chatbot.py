import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        
        # Grid configurations to position elements on the gui
        self.grid_columnconfigure(0, weight=1) # Configure column
        self.grid_rowconfigure(1, weight=1)  # Configure row
                
        # Title of the app
        self.title = customtkinter.CTkLabel(self, text="Hello, I'm a chatbot!")
        self.title.grid(row=0, column=1, pady=10, sticky="nsew")
        
        # Entry for the user to enter their message to the chatbot
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter your message here")
        # Positioned bottom centre
        self.entry.grid(row=1, column=0, padx=5, pady=10, sticky="sew")
        # Positioned bottom right
        self.send_message_button = customtkinter.CTkButton(self, text="Send message", command=self.send_message) 
        self.send_message_button.grid(row=1, column=1, padx=5, pady=10, sticky="sew")
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=200, height=200)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="new")
        
        
    def new_bubble(self, message, sender):
        # Create a new bubble
        bubble = customtkinter.CTkBubble(self, text=message, sender=sender)
        # Add the bubble to the chat
        self.chat.add_bubble(bubble
        )
    def send_response(self, response):
        print(response)
        
    def send_message(self):
        # Get the message from the entry
        message = self.entry.get()
        # Clear the entry
        self.new_bubble(message, "user")
        self.entry.delete(0, 'end')
        print("button clicked")


app = App()
app.mainloop()