#!/usr/bin/env python
from io import StringIO
import os
import sys, getopt
from googletrans import Translator

#Gets the size of the file in characters
def getfilesize(filename):
    lines=0
    words=0
    characters=0
    with open(filename) as infile:
        for line in infile:
            wordslist=line.split()
            lines=lines+1
            words=words+len(wordslist)
            characters += sum(len(word) for word in wordslist)
    return characters

#Splits the file in chunks of 10000 characters, translates the chunks and then combines everything into one file
def splitfile(filename):
   translator = Translator()
   translationText = ''
   # Open original file in read only mode
   if not os.path.isfile(filename):
       print("No such file as: \"%s\"" % filename)
       return

   step = 10000
   finalStep = 0
   slice = []
   data = open(filename, 'r', encoding='utf-8').read()
   for i in range(0, getfilesize(filename), 10000):
        finalStep = step
        slice = data[i:step]
        step += 10000
        translation =translator.translate(slice, dest='en')
        translationText += translation.text
   if((finalStep-10000)<getfilesize(filename)):
       slice= data[finalStep:]
       translation = translator.translate(slice, dest='en')
       translationText += translation.text
   return translationText

def convertMultiple(engDir, norDir):
    translator = Translator()
    translationText = ''
    if norDir == "": norDir = os.getcwd() + "\\" #if no pdfDir passed in
    for txt in os.listdir(norDir): #iterate through pdfs in pdf directory
        norTxtFilename = norDir + txt
        fileCharSize = getfilesize(norTxtFilename)
        if(fileCharSize>14999):
            translationText = splitfile(norTxtFilename)
        else :
            data = open(norTxtFilename, 'r').read()
            translation =translator.translate(data, dest='en')
            translationText = translation.text
        textFilename = engDir + txt
        textFile = open(textFilename, "w", encoding='utf-8') #make text file
        textFile.write(translationText) #write text to text file

engDir = "C:\\Bo\\python-translation-project\\english\\"
norDir = "C:\\Bo\\python-translation-project\\norwegian\\"
convertMultiple(engDir, norDir)
