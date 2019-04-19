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
            print("Language (" + name + ") not supported!")
            sys.exit(1)
        
        if allOp != None or textOp != None or languageOp != None or fullOp != None:
            if "sentiment2" in tasksSupported:

                #download necessary files, quiet=True for not outputing download info to stdout
                downloader.download("sentiment2." + lang, quiet=True)
                
                if allOp != None or textOp != None or fullOp != None:
                    sumSentiment = 0
                    numberWords = 0
                    for word in parsedText.words:
                        numberWords += 1
                        sumSentiment += word.polarity
                
                if allOp != None or languageOp != None:
                    print("Language detected: " + name)

                if allOp != None or textOp != None:
                    print("\nSentiment of text:")
                    print("\tsum: " + str(sumSentiment))
                    print("\tmean: " + str(sumSentiment/numberWords))

            else:
                print("Language (" + name + ") not supported!")
                sys.exit(1)

        if allOp != None or entityOp != None or fullOp != None:
            if "ner2" in tasksSupported and "embeddings2" in tasksSupported:

                #download necessary files, quiet=True for not outputing download info to stdout
                downloader.download("ner2." + lang, quiet=True)
                downloader.download("embeddings2." + lang, quiet=True)

                if entityOp != None or allOp != None:
                    print("\nSentiment associated to each entity by order of appearance in text:")
                for entity in parsedText.entities:
                    entitySent = entity.positive_sentiment-entity.negative_sentiment
                    if fullOp != None or allOp != None:
                        sumSentiment += entitySent

                    if entityOp != None or allOp != None:
                        print("\t" + str(" ".join(entity)) + ": " + str(entitySent))
            
                if fullOp != None or allOp != None:
                    print("\nFinal Sentiment of text (with entity sentiment):")
                    print("\tsum: " + str(sumSentiment))
                    print("\tmean: " + str(sumSentiment/numberWords))

            else:
                print("Language (" + name + ") not supported!")
                sys.exit(1)
    else:
        print("Can't detect language reliably or don't support language!")
        sys.exit(1)

def printHelp():
    print("Usage: ./Polymotions.py [OPTIONS] [FILENAME]")
    print("  or:  ./Polymotions.py [OPTIONS]")
    print("Default behaviour: ")
    print("\nOptions:")
    print("  -h\tHelp")
    print("\nExample: ./Polymotions.py text.txt")

#main

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'atefhl')
    dict_opts = dict(options)
except:
    printHelp()
    sys.exit(1)

helpOp = dict_opts.get('-h',None)
allOp = dict_opts.get('-a',None)
languageOp = dict_opts.get('-l',None)
textOp = dict_opts.get('-t',None)
fullOp = dict_opts.get('-f',None)
entityOp = dict_opts.get('-e',None)

if helpOp!=None:
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
