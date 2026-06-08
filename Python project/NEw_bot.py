import speech_recognition as sr
import pyttsx3
import pywhatkit
import os
from fpdf import FPDF

# Initialize the recognizer and speaker
listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice).lower()
        print("You said:", command)
        return command

def run_assistant():
    command = listen_command()

    if command is None:
        talk("I didn't catch that. Please try again.")
        return

    command = command.lower()

    # YouTube Search
    if "youtube" in command or "search" in command:
        # Look for "search" or "youtube" and get what's after
        if "search for" in command:
            search_term = command.split("search for", 1)[1].strip()
        elif "search" in command:
            search_term = command.split("search", 1)[1].strip()
        elif "youtube" in command:
            search_term = command.split("youtube", 1)[1].strip()
        else:
            search_term = ""

        if search_term:
            talk(f"Searching YouTube for {search_term}")
            pywhatkit.playonyt(search_term)
        else:
            talk("What do you want me to search for on YouTube?")


    elif "create pdf" in command:
        talk("What should I write in the PDF?")
        text = listen_command()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output("output.pdf")
        talk("PDF created successfully")

    elif "open" in command:
        app_or_file = command.replace("open", "").strip()
        talk(f"Opening {app_or_file}")
        os.system(f'start {app_or_file}')

    else:
        talk("Sorry, I didn't understand that.")

# Run the assistant
run_assistant()