from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from pydub import AudioSegment
#import pyttsx3
import vlc
from gtts import gTTS
import speech_recognition as sr
import re
from os import path
import time

def convertAudio(srcType, desType, inFile, outFile):
    # files
    src = inFile
    dst = outFile

    # convert wav to mp3
    audSeg = AudioSegment.from_mp3(inFile)
    audSeg.export(dst, format=(desType))

def speakText(text, saveName, speak=True):    
    spokenContent = gTTS(text)
    spokenContent.save(saveName)
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(saveName)
    player.set_media(media)        
    if speak == True:  
        player.play()
        time.sleep(1)
        duration = player.get_length()
        time.sleep(duration//1000)
    return

def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        text = r.recognize_google(audio)
    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text

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

def wikiMe(text=False, save=True):
    primer = 'http://en.wikipedia.org/wiki/'
    if text:
       unformat = input('What do you want know about? \n').replace(' ', '_')
       queryTerm = unformat.lower()
    if text == False:
        speakText('what do you want to know about', 'WebScraper/question.txt', True)
        queryTerm = speechToText()
    fullUrl = primer + queryTerm
    # print(fullUrl)
    hasRef = webScoop(fullUrl, 'p', show=False)
    hasPronounce = re.sub('\[(.*?)\]', '', hasRef)
    hasDubPar = re.sub('\/(.*?)\/', '', hasPronounce)    
    hasDubSpace = re.sub('\( \((.*?)\)\)', '', hasDubPar)
    cleanText = re.sub(' +', ' ', hasDubSpace)
    if text:
        print(cleanText)
        if save:
            name = 'WebScraper' + input('Save as: ') + '.txt'
            file = open('WebScraper/'+name, "a", encoding='utf-8')
            file.write(cleanText)
            file.close()
    elif text == False:
        if save == False:
            speakText(cleanText, 'WebScraper/wikispeak')
        elif save:
            name = 'WebScraper/' + input('Save as: ') + '.txt'
            speakText(cleanText, name)

wikiMe()
