from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from pydub import AudioSegment
from pydub.playback import play
import re
import pyaudio
import wave
from os import path
from pvrecorder import PvRecorder
import pyttsx3
import whisper

def convertAudio(srcType, desType, inFile, outFile):
    # files
    src = inFile
    dst = outFile

    # convert wav to mp3
    audSeg = AudioSegment.from_mp3(inFile)
    audSeg.export(dst, format=(desType))

def speakText(text, voice, saveName, speak=True, saveToFile=True):    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    if saveToFile == True:
        engine.save_to_file(text, saveName)
    if speak == True:

        engine.say(text)
    engine.runAndWait()
    engine.stop()

def speechToText():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    model = whisper.load_model("base")
    result = model.transcribe("output.wav")
    print(result["text"])
    return result["text"]



def webScoop(webAdress, contentSweep, show=True):
    output = str()
    req = Request(webAdress, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    soup = BeautifulSoup(webpage, 'html.parser')
    # if show == True:
    #     print(soup.title.string)
    # output = output + soup.title.string
    paragraphs = soup.find_all(contentSweep)
    if show == True:
        print(len(paragraphs))
    for i in paragraphs:
        text = i.getText()
        if show == True:
            print(text)
        output = output + text
    return output

def wikiMe(text=False):
    primer = 'https://en.wikipedia.org/wiki/'
    if text:
       unformat = input('What do you want know about? \n').replace(' ', '_')
       query = unformat.lower()
       queryTerm = re.sub(r'([^\s])\s([^\s])', r'\1_\2', query)
    if text == False:
        speakText('what do you want to know about', 1, '', True, False)
        query = speechToText()
        #queryTerm = re.sub(r'([^\s])\s([^\s])', r'\1_\2', query)
        queryWithSpace = query.replace(' ','')
        queryTerm = queryWithSpace.replace('.','')
    fullUrl = primer + queryTerm
    print(fullUrl)
    hasRef = webScoop(fullUrl, 'p', show=False)
    hasPronounce = re.sub('\[(.*?)\]', '', hasRef)
    hasDubPar = re.sub('\/(.*?)\/', '', hasPronounce)    
    hasDubSpace = re.sub('\( \((.*?)\)\)', '', hasDubPar)
    cleanText = re.sub(' +', ' ', hasDubSpace)
    if text:
        choice = input('Do you want to save? [Y/n]: ')
        if choice == 'Y' or 'y':
            save = True
        elif choice == 'N' or 'n':
            save = False 
        if save:
            name = input('Save as: ') + '.txt'     
            file = open(name, "w", encoding='utf-8')
            file.write(cleanText)
            file.close() 
        print(cleanText)
    elif text == False:
        speakText('Do you want to save?', 1, '', True, False)
        print("please say yes or no")
        response = speechToText()
        responseNoPunct = re.sub('[^\w]', '', response)
        choice = responseNoPunct.lower()
        print(choice)
        if choice == 'yes':   
            speakText('What would you like to call it:', 1, '', True, False)
            badName = speechToText()
            okName = badName.replace(' ', '_')
            goodName = re.sub('[^\w]','',okName)
            textName = goodName + '.txt'     
            wavName = goodName + '.wav'     
            file = open(textName, "w", encoding='utf-8')
            file.write(cleanText)
            file.close() 
            speakText(cleanText, 1, wavName, True, True)
        elif choice == 'no':
            speakText(cleanText, 1, '', True, False)

wikiMe()
