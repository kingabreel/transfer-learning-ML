from gtts import gTTS

def getSomeText():
    text_to_say = input("Which phrase would you like to convert?\n")
    print("\nNow which language is the phrase?\n")
    language = input("en, pt\n")

    if language == 'en' or language == 'pt':
        gtts_object = gTTS(text = text_to_say,
                    lang = language,
                    slow = False)
        
        gtts_object.save("./gtts.wav")

getSomeText()