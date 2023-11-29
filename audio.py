import speech_recognition as sr
import pyaudio
import wave
from googletrans import Translator
from gtts import gTTS
import os 

FORMAT = pyaudio.paInt16
CHANNELS = 1 # Mono audio
RATE = 44100 # sample rate
CHUNK = 1024 # size of each audio chunk
RECORD_SECONDS = 5 # Duration to record Mic input
OUTPUT_FILE = "output.wav"

def text_to_speech(text, language='es', filename ='output.mp3'):
        tts = gTTS(text = text, lang=language, slow=False)
        tts.save(filename)
        os.system('mpg321 ' + filename)


# Test With USB Mic plugged in
def recognize_speech():
        audio = pyaudio.PyAudio()

        try:
                stream = audio.open(format=FORMAT, 
                                        channels=CHANNELS,
                                        rate=RATE,input=True,
                                        frames_per_buffer=CHUNK)
                print("Recording now")
                text_to_speech("Recording now")
                frame = []

                # Capture audio for specified duration
                for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frame.append(data)

                # Stop  audio stream
                stream.stop_stream()
                stream.close()
                print(f"Recording stopped. You said {frame}")

 		# Terminate PyAudio session
                audio.terminate()

                # Write recorded audio to WAV output file
                with wave.open(OUTPUT_FILE, "wb") as wf:
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(audio.get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b"".join(frame))

                print("Audio saved")

                # Recognizing speech on WAV File, convert to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(OUTPUT_FILE) as source:
                        data = recognizer.record(source)

                text = recognizer.recognize_google(data)
                print(text)
                return text

        except sr.UnknownValueError:
                sorry = "Sorry, I couldn't understand."
                print(sorry)
                text_to_speech(sorry)
                return None

        except sr.RequestError as e:
                print(f"Error with the recognition service; {e}")
                return None


# Need to change API to Google Cloud Translate API  
def translate_text(text, target_language='es'):
        translator = Translator()
        translation = translator.translate(text, src='en', dest='es')
        print(translation.text)
        return translation.text

if __name__ == "__main__":
        english_text = recognize_speech()
        if english_text:
                print(english_text)
                spanish_text = translate_text(text=english_text)
                text_to_speech(text=spanish_text, language='es')

#       text = "Hello, World! My name is Rasberry asjkdhfg."
#       text_to_speech(text)

