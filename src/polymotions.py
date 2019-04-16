#!/usr/bin/env python3

import re, sys, getopt, polyglot
from polyglot.text import Text
from polyglot.downloader import downloader

def getSentiments(text):
    parsedText = Text(text)

    lang = parsedText.language.code
    name = parsedText.language.name
    if(parsedText.language.confidence>95):
        try:
            tasksSupported = downloader.supported_tasks(lang=lang)
        except:
            print("Language (" + name + ") don't supported!")
            sys.exit(1)

        if "sentiment2" in tasksSupported:

            #download necessary files, quiet=True for not outputing download info to stdout
            downloader.download("sentiment2." + lang, quiet=True)
    
            sumSentiment = 0
            for word in parsedText.words:
                sumSentiment += word.polarity

            print("Language detected: " + name)
            print("Sentiment of text: " + str(sumSentiment))

        else:
            print("Language (" + name + ") don't supported!")
    else:
        print("Can't detect language reliably or don't support language!")

def printHelp():
    print("Usage: ./Polymotions.py [OPTIONS] [FILENAME]")
    print("  or:  ./Polymotions.py [OPTIONS]")
    print("Default behaviour: ")
    print("\nOptions:")
    print("  -h\tHelp")
    print("\nExample: ./Polymotions.py text.txt")

#main

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'h')
    dict_opts = dict(options)
except:
    printHelp()
    sys.exit(1)

help = dict_opts.get('-h',None)

if help!=None:
    printHelp()
    sys.exit(1)
else:
    # read from STDIN if file is not passed as argument
    if remainder:
        try:
            input = open(remainder[0])
        except:
            print("Wrong file path! File doesn't exist?")
            printHelp()
            sys.exit(1)
    else:
        input = sys.stdin

    try:
        content = input.read()
    except:
        print("\nUse CTRL+D instead to get results!")
        sys.exit(1)

    getSentiments(content)
