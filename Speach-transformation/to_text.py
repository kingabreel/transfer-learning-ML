import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import playsound
import wikipedia
import webbrowser

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

def respond(text):
    print("Text from get audio " + text)
    if 'youtube' in text:
        speak("In one word, what do you'd like to search?")
        keyword = get_audio()
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            speak(f"Here is what I have found for {keyword} on youtube")
    elif 'search' in text:
        speak("In one word, what do you'd like to search?")
        query = get_audio()
        if query !='':
            result = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            print(result)
            speak(result)
    elif 'what time' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(strTime)
    elif 'spotify' in text or 'play song' in text:
        speak("Openning spotify")
        url = "https://open.spotify.com"
        webbrowser.get().open(url)
    elif 'save audio' in text or 'audio to file' in text:
        speak("You can start to speak now what do you want to save in text")
        phrase = get_audio();
        
        if phrase != '':
            with open("result.txt", "w") as file:
                file.write(phrase)
                speak("File saved")

    elif 'exit' in text:
        speak("Goodbye, till next time")
        exit()

while True:
    print("I am listening...")
    text = get_audio()
    respond(text)