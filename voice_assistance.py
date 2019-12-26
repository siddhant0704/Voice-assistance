import fitz
import json
import re
import heapq
import os
import numpy as np
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import webbrowser as wb
import speech_recognition as sr
from Find_tags import find_tags
import operator
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 110)

def calc(l,l1):
    c = 0
    for word in l:
        if word in l1:
            c = c + 1

    k = len(l)
    r = (c / k) * 100
    print(r)

def find_title(pdf):
    doc = fitz.open(pdf)
    page = doc.getPageText(0, output="json")
    max_size = 0
    blocks = json.loads(page)["blocks"]
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    size = span["size"]
                    if size > max_size:
                        max_size = size

    bboxList = {}
    title = ""
    blocks = json.loads(page)["blocks"]
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    line_text = span["text"]
                    text_size = span["size"]
                    if text_size == max_size:
                        title = title + " " + line_text


    return title

print(find_title("A2.pdf"))
m=find_title("A2.pdf")
m=re.sub(' +',' ',m)

m=m.strip()
print(m)
li = list(m.split(" "))
print(li)

with open('BG1.txt') as file:

    contents = file.read()

    l1=[]

    ps = PorterStemmer()
    review = [word for word in li if not word in set(stopwords.words('english'))]
    review = [word.capitalize() for word in review]
    for word in review:
        if word in contents:
            l1.append(word)

    print(l1)

# initialised for proper no of times the machine speaks to the user
m=0
n=0
def speak(m,n):
    with open('BG1.txt') as file:

            contents = file.read()

            r1=sr.Recognizer()
            r2=sr.Recognizer()
            r3=sr.Recognizer()

            l=[]
            with sr.Microphone() as source:
                engine.say("Speak now")
                engine.runAndWait()
                audio=r3.listen(source)
                try:
                    print(r1.recognize_google(audio, show_all=True))
                    review = re.sub('[^a-zA-Z]', ' ', r1.recognize_google(audio))
                    review = review.split()
                    ps = PorterStemmer()
                    review = [word for word in review if not word in set(stopwords.words('english'))]
                    review = [word.capitalize() for word in review]
                    print(review)
                    l = review

                    c = find_tags("A2.pdf")

                    # Calculating score of the pdf
                    sum = 0
                    for i in l:
                        if i in c['title']:
                            # if tag in title add 1
                            sum = sum + 1

                        if i in c['normalTags']['Country']:
                            p1 = c['normalTags']['Country'][i]
                            p11 = c['normalTags']['Country']
                            # finding max freq in that dictionary
                            n1 = max(p11.items(), key=operator.itemgetter(1))[0]
                            n11 = c['normalTags']['Country'][n1]
                            # normalising the ones not in the title
                            s1 = p1 / n11
                            sum = sum + s1
                        elif i in c['normalTags']['Companies']:
                            p2 = c['normalTags']['Companies'][i]
                            p21 = c['normalTags']['Companies']
                            # finding max freq in that dictionary
                            n2 = max(p21.items(), key=operator.itemgetter(1))[0]
                            n21 = c['normalTags']['Companies'][n2]
                            # normalising the ones not in the title
                            s2 = p2 / n21
                            sum = sum + s2

                        elif i in c['normalTags']['Industry']:
                            p3 = c['normalTags']['Industry'][i]
                            p31 = c['normalTags']['Industry']
                            # finding max freq in that dictionary
                            n3 = max(p31.items(), key=operator.itemgetter(1))[0]
                            n31 = c['normalTags']['Industry'][n3]
                            # normalising the ones not in the title
                            s3 = p3 / n31
                            sum = sum + s3

                        elif i in c['normalTags']['Technology']:
                            p4 = c['normalTags']['Technology'][i]
                            p41 = c['normalTags']['Technology']
                            # normalising the ones not in the title
                            n4 = max(p41.items(), key=operator.itemgetter(1))[0]
                            n41 = c['normalTags']['Technology'][n4]
                            # finding max freq in that dictionary
                            s4 = p4 / n41
                            sum = sum + s4

                    print(sum)

                #in case the person doesn't say anything we pop up and exeption
                except sr.UnknownValueError:
                    if len(l) == 0:
                        m = m + 1
                        if m < 2:
                            if n<m:
                                engine.say("Please speak again")
                                n=n+1

                            speak(m,n)
                        else:
                            engine.say("try again")
                            engine.runAndWait()
                            exit()

                #in case there is no internet connection, exception is popped
                except sr.RequestError:
                    engine.say("please check your internet connection")
                    engine.runAndWait()
                    exit()

speak(0,0)
