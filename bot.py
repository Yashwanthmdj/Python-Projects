import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import smtplib
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set property 'voice', not 'voices'

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'bot' in command:
                command = command.replace('bot', '')
                print(command)
    except:
        pass
    return command

def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('yashwanthmdj@Gmail.com', 'Ronaldo@2024')
    server.sendmail('yashwanthmdj@Gmail.com', receiver, f"Subject: {subject}\n\n{message}")
    server.quit()

def get_weather(city):
    api_key = 'your_openweathermap_api_key'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    weather_data = response.json()
    if weather_data['cod'] == 200:
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"The weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, unable to fetch weather information."

def run_bot():
    command = take_command()
    print(command)
    if 'Hello py' in command:
        talk('Hello user , Welcome to the virtual assistance..')
        exit()
    if 'Good moring' in command :
        talk('A very Good morning User !')
        exit()
    if 'stop' in command:
            talk('Goodbye! If any more usage please run me again')
            exit()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('Who the heck is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        talk('The date is ' + date)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'search' in command:
        query = command.replace('search', '')
        talk('Searching Google for ' + query)
        pywhatkit.search(query)
    elif 'note' in command:
        talk('What do you want to note down?')
        note_text = take_command()
        with open('notes.txt', 'a') as f:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ' + note_text + '\n')
        talk('Note added to Notepad.')
    elif 'location' in command:
        talk('Sorry, location feature is not available yet.')
    elif 'call' in command:
        contact_name = command.replace('call', '').strip()
        talk(f'Calling {contact_name}')
        # Calling feature
    elif 'send email' in command:
        talk('To whom should I send the email?')
        recipient = take_command()
        talk('What is the subject of the email?')
        subject = take_command()
        talk('What should I say in the email?')
        message = take_command()
        send_email(recipient, subject, message)
        talk('Email sent successfully.')
    elif 'weather' in command:
        talk('Which city do you want the weather information for?')
        city = take_command()
        weather_info = get_weather(city)
        talk(weather_info)
    elif 'calculate' in command:
        expression = command.replace('calculate', '').strip()
        result = eval(expression)
        talk(f'The result of {expression} is {result}')
    else:
        talk('Any more information you want to know ? !')

while True:
    run_bot()
