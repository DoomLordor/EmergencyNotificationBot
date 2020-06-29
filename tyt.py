import os
from pydub import AudioSegment
import soundfile as sf
import speech_recognition as sr
AudioSegment.converter="D:/ХАКАТОН/ffmpeg/bin/ffmpeg.exe"
r = sr.Recognizer ()
name = 'sound'
path = os.path.join(os.getcwd(), name)
sound = AudioSegment.from_file(f'{os.getcwd()}\{name}.ogg')
sound.export(path.replace('.ogg', '.wav'), format="wav")
#data, samplerate = sf.read('D:/ХАКАТОН/sound.ogg')
#sf.write('D:/ХАКАТОН/sound.wav', data, samplerate)
f = sr.AudioFile('D:/ХАКАТОН/sound')
with f as audio_file:
  audio_content = r.record(audio_file)
  zadanie = r.recognize_google(audio_content, language="Ru-r")
  print(format(zadanie))