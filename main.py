import datetime
import re
import random
import tkinter as tk
from tkinter import scrolledtext, ttk


# Define a function to get a greeting based on the time of day
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"


# Define a function to perform basic arithmetic operations
def perform_arithmetic(operation, num1, num2):
    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            return num1 / num2
        else:
            return "Cannot divide by zero."
    else:
        return "Unsupported operation."


# Chatbot response function
def chatbot_response(user_input):
    user_input = user_input.lower()

    patterns = [
        (r"my name is (.*)", "Hello {0}! Nice to meet you."),
        (r"hi|hey|hello", f"{get_greeting()} How can I assist you today?"),
        (r"what is your name", "I'm ChatBot, your virtual assistant."),
        (r"how are you", "I'm just a program, but I'm doing great! How about you?"),
        (r"(add|subtract|multiply|divide) (\d+(\.\d+)?) and (\d+(\.\d+)?)",
         lambda m: f"The result is {perform_arithmetic(m.group(1), float(m.group(2)), float(m.group(4)))}"),
        (r"tell me a joke", random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What did one ocean say to the other ocean? Nothing, they just waved.",
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "Why don’t programmers like nature? It has too many bugs.",
            "What do you call fake spaghetti? An impasta.",
            "I asked the librarian if the library had any books on paranoia. She whispered, 'They're right behind you.'",
            "Why don’t eggs tell jokes? They might crack up.",
            "Why did the computer go to the doctor? Because it had a virus!"
        ])),
        (r"tell me a quote", random.choice([
            "Believe you can and you're halfway there.",
            "Act as if what you do makes a difference. It does.",
            "In the middle of every difficulty lies opportunity.",
            "It always seems impossible until it's done.",
            "The only way to do great work is to love what you do.",
            "The best time to plant a tree was 20 years ago. The second best time is now.",
            "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "Your time is limited, so don’t waste it living someone else’s life.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "You miss 100% of the shots you don’t take."
        ])),
        (r"quit", "Goodbye! Take care."),
    ]

    for pattern, *responses in patterns:
        match = re.match(pattern, user_input)
        if match:
            if callable(responses[0]):
                return responses[0](match)
            return random.choice(responses).format(*match.groups())

    return "I'm not sure I understand. Can you rephrase that?"


# GUI implementation using Tkinter
def chatbot_gui():
    # Default theme: Light
    theme = "light"

    # Define the send function
    def send():
        user_message = user_input.get()
        if user_message.strip():
            chat_display.config(state="normal")
            chat_display.insert(tk.END, f"You: {user_message}\n", "user")
            chat_display.config(state="disabled")
            chat_display.yview(tk.END)
            chat_display.after(1000, display_bot_response, user_message)

        user_input.delete(0, tk.END)

    def display_bot_response(user_message):
        response = chatbot_response(user_message)
        chat_display.config(state="normal")
        chat_display.insert(tk.END, f"ChatBot: {response}\n", "bot")
        chat_display.config(state="disabled")
        chat_display.yview(tk.END)

    def switch_theme():
        nonlocal theme
        if theme == "light":
            theme = "dark"
            root.config(bg="#333333")
            header.config(bg="#444444", fg="white")
            chat_display.config(bg="#555555", fg="white")
            chat_display.tag_config("user", foreground="#1E90FF", font=("Arial", 12, "bold"))
            chat_display.tag_config("bot", foreground="#8A2BE2", font=("Arial", 12))
            user_input.config(bg="#444444", fg="white")
            send_button.config(bg="#FF1493", fg="white")
            joke_button.config(bg="#ADD8E6", fg="black")
            quote_button.config(bg="#FF6347", fg="white")
            exit_button.config(bg="#DC143C", fg="white")
        else:
            theme = "light"
            root.config(bg="#D8B4DD")  # Light pastel background
            header.config(bg="#FF69B4", fg="white")
            chat_display.config(bg="#F5FFFA", fg="#2E8B57")
            chat_display.tag_config("user", foreground="#1E90FF", font=("Arial", 12, "bold"))  # Blue for user
            chat_display.tag_config("bot", foreground="#8A2BE2", font=("Arial", 12))  # Purple for bot
            user_input.config(bg="#FFFAFA", fg="#2E8B57")
            send_button.config(bg="#FF1493", fg="white")
            joke_button.config(bg="#FFB6C1", fg="black")
            quote_button.config(bg="#FF6347", fg="white")
            exit_button.config(bg="#DC143C", fg="white")

    # Close the application
    def exit_app():
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("ChatBot")
    root.geometry("500x600")
    root.config(bg="#D8B4DD")  # Light pastel background

    # Add Chatbot Avatar
    avatar = tk.PhotoImage(file="Chatbot Chat Message.png")  # Replace with your image file
    avatar_label = tk.Label(root, image=avatar, bg="#f0f8ff")
    avatar_label.pack(pady=10)

    # Header Label
    header = tk.Label(root, text="ChatMate – Your conversational companion", bg="#FF69B4", fg="white",  # Light pink
                      font=("Arial", 16, "bold"), pady=10)
    header.pack(fill=tk.X)

    # Chat display area
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", height=25, bg="#F5FFFA",  # Mint green background
                                             fg="#2E8B57", font=("Arial", 12))
    chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Add tags for styling
    chat_display.tag_config("user", foreground="#1E90FF", font=("Arial", 12, "bold"))  # Blue for user
    chat_display.tag_config("bot", foreground="#8A2BE2", font=("Arial", 12))  # Purple for bot

    # Input field and send button
    input_frame = tk.Frame(root, bg="#f0f8ff")
    input_frame.pack(pady=10, fill=tk.X)

    user_input = tk.Entry(input_frame, font=("Arial", 14), width=40, bg="#FFFAFA", fg="#2E8B57")  # Light background
    user_input.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

    send_button = tk.Button(input_frame, text="Send", command=send, bg="#FF1493", fg="white",  # Hot pink button
                            font=("Arial", 12, "bold"), width=10)
    send_button.pack(side=tk.RIGHT, padx=5)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=exit_app, bg="#DC143C", fg="white",  # Crimson color for exit
                            font=("Arial", 12, "bold"))
    exit_button.pack(pady=5)

    # Buttons for jokes, quotes, and theme switching
    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=5, fill=tk.X)

    joke_button = tk.Button(button_frame, text="Tell me a Joke", command=lambda: display_bot_response("tell me a joke"),
                            bg="#FFB6C1", font=("Arial", 12), width=15)  # Light pink for jokes
    joke_button.pack(side=tk.LEFT, padx=5)

    quote_button = tk.Button(button_frame, text="Tell me a Quote", command=lambda: display_bot_response("tell me a quote"),
                             bg="#FF6347", font=("Arial", 12), width=15)  # Light red for quotes
    quote_button.pack(side=tk.LEFT, padx=5)

    theme_button = tk.Button(button_frame, text="Switch Theme", command=switch_theme,
                             bg="#ADD8E6", font=("Arial", 12), width=15)  # Light blue for theme
    theme_button.pack(side=tk.LEFT, padx=5)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    chatbot_gui()
