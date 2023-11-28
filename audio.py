import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os 

def text_to_speech(text, language='es', filename ='output.mp3'):
	tts = gTTS(text = text, lang=language, slow=False)
	tts.save(filename)
	os.system('mpg321 ' + filename)


def recognize_speech():
	recognizer = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something in English")
		audio = recognizer.listen(source)

	try:
		text = recognizer.recognize_google(audio)
		text_to_speech(f"You said, {text}")
		return text
	except sr.UnknownValueError:
		sorry = "Sorry, I couldn't understand."
		print(sorry)
		text_to_speech(sorry)
		return None
	except sr.RequestError as e:
		print(f"Error with the recognition service; {e}")
		return None

def translate_text(text, target_language='es'):
	translator = Translator()
	translation = translator.translate(text=text, dest='es')
	print(translation)
	return translation.text


if __name__ == "__main__":
	english_text = "Hello World!"
	if english_text:
		print(english_text)
#		spanish_text = translate_text(text=english_text)
		text_to_speech(text='Hola!Vamos. Si se Puede', language='es')

#	text = "Hello, World! My name is Rasberry asjkdhfg."
#	text_to_speech(text)
