#!/usr/bin/env python3

import re, sys, getopt, polyglot
from polyglot.text import Text
from polyglot.downloader import downloader

def textSentiment(parsedText,lang):
    #download necessary files, quiet=True for not outputing download info to stdout
    downloader.download("sentiment2." + lang, quiet=True)
    
    if allOp != None or textOp != None or fullOp != None:
        sumSentiment = 0
        numberWords = 0
        for word in parsedText.words:
            numberWords += 1
            sumSentiment += word.polarity
    
    if allOp != None or textOp != None:
        print("\nSentiment of text:")
        print("\tsum: " + str(sumSentiment))
        print("\tmean: " + str(sumSentiment/numberWords))

    return (sumSentiment,numberWords)

def entitiesAndFinalSentiment(parsedText,lang,sumSentiment,numberWords):
    #download necessary files, quiet=True for not outputing download info to stdout
    downloader.download("ner2." + lang, quiet=True)
    downloader.download("embeddings2." + lang, quiet=True)

    if entityOp != None or allOp != None:
        print("\nSentiment associated to each entity by order of appearance in text:")
    
    if findOp != None:
        findsSent = 0
        findsOcur = 0
        findsOut = ""

    for entity in parsedText.entities:
        entitySent = entity.positive_sentiment-entity.negative_sentiment
        if fullOp != None or allOp != None:
            sumSentiment += entitySent

        if entityOp != None or allOp != None:
            print("\t" + str(" ".join(entity)) + ": " + str(entitySent))
        if findOp != None:
            jEntity = " ".join(entity)
            if findOp in jEntity:
                findsOut += "\t" + jEntity + ": " + str(entitySent) + "\n"
                findsSent += entitySent
                findsOcur += 1

    if findOp != None:
        print("\nOcurences and sentiment of \"" + findOp + "\" entity:")
        print(findsOut, end='') #print without newline
        print("\nTotal of \"" + findOp + "\" entity:")
        print("\tsum: " + str(findsSent))
        print("\tmean: " + str(findsSent/findsOcur))

    if fullOp != None or allOp != None:
        print("\nFinal Sentiment of text (with entity sentiment):")
        print("\tsum: " + str(sumSentiment))
        print("\tmean: " + str(sumSentiment/numberWords))

def getSentiments(text):
    parsedText = Text(text)

    lang = parsedText.language.code
    name = parsedText.language.name

    if(parsedText.language.confidence>95):
        if allOp != None or languageOp != None:
            print("Language detected: " + name)

        if allOp != None or textOp != None or fullOp != None or entityOp != None or findOp != None:
            try:
                tasksSupported = downloader.supported_tasks(lang=lang)
            except:
                print("Language (" + name + ") not supported!")
                sys.exit(1)
        
        if allOp != None or textOp != None or fullOp != None:
            if "sentiment2" in tasksSupported:
                (sumSentiment, numberWords) = textSentiment(parsedText,lang)
            else:
                print("Language (" + name + ") not supported!")
                sys.exit(1)

        if allOp != None or entityOp != None or fullOp != None or findOp != None:
            if "ner2" in tasksSupported and "embeddings2" in tasksSupported:
                if 'sumSentiment' not in locals():
                        sumSentiment = 0
                if 'numberWords' not in locals():
                        numberWords = 0
                entitiesAndFinalSentiment(parsedText,lang,sumSentiment,numberWords)
            else:
                print("Language (" + name + ") not supported!")
                sys.exit(1)
    else:
        print("Can't detect language reliably or don't support language!")
        sys.exit(1)

def printHelp():
    print("Usage: ./Polymotions.py [OPTIONS] [FILENAME]")
    print("  or:  ./Polymotions.py [OPTIONS]")
    print("Default behaviour: Obtains the sentiment of text with the entities sentiment")
    print("\nOptions:")
    print("  -l\tDetect language of text")
    print("  -t\tObtains sentiment of text")
    print("  -e\tObtains sentiment of entities of text")
    print("  -f\tGet the sentiment for the entity passed by argument")
    print("  -a\tAll above except '-f'")
    print("  -h\tHelp")
    print("\nExample: ./Polymotions.py text.txt")
    print("\nExample: ./polymotions.py -f Paris text.txt")

#main

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'atehlf:')
    dict_opts = dict(options)
except:
    printHelp()
    sys.exit(1)

helpOp = dict_opts.get('-h',None)
allOp = dict_opts.get('-a',None)
languageOp = dict_opts.get('-l',None)
textOp = dict_opts.get('-t',None)
findOp = dict_opts.get('-f',None)
entityOp = dict_opts.get('-e',None)

# Default behaviour
if not dict_opts:
    fullOp = ' '
else:
    fullOp = None

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
