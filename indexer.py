import os
import sys
import gzip
import json
import csv
import time
def main():
    
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'trainQueries.tsv'
    outputFolder = sys.argv[3] if argv_len >= 4 else 'results/'
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
 
    with gzip.open(inputFile) as unzippedFile:
        fileData = json.load(unzippedFile)
        fileData = fileData["corpus"]
    
    invertedIndex = createInvertedList(fileData)
    with open(queriesFile) as queries:
        queriesData = csv.reader(queries,delimiter="\t")
        for row in queriesData:
            time1 = time.perf_counter()
            a = evaluate(row,invertedIndex,fileData)
            print(a)
            a.sort()
            print(a)
            opFile = open(outputFolder + row[0]+'.txt','w')
            for i in a:
                opFile.write(str(i)+ "\n")
            time2 = time.perf_counter()
            print(row[0],time2-time1)

def getPlayId(sNum,fd):
    for i in fd:
        if i["sceneNum"] == sNum:
            return i["playId"]

def getSceneId(sNum,fd):
    for i in fd:
        if i["sceneNum"] == sNum:
            return i["sceneId"]

def evaluate(r,ii,fd):
    foundScenes = []
    wordIndex = []
    foundPhrases = []
    sceneOrPlay = ""
    finalList = []
    andFlag = False
    orFlag = False
    number = 0
    for word in r:
        if number == 0:
            print()
        elif number == 1:
            sceneOrPlay = word
        elif number == 2:
            if word == "and":
                andFlag = True
            elif word == "or":
                orFlag = True
        elif " " in word:
            newWords = word.split()
            for newWord in newWords:
                if newWord in ii.keys() :   
                    tempIndex = ii[newWord]
                else:
                    tempIndex=[]               
                if wordIndex == []:
                    wordIndex = tempIndex
                else:
                    consecutiveWordIndex = []
                    for i in tempIndex:
                        for j in wordIndex:
                            if i[0] == j[0]:
                                if i[1] - j[1] == 1:
                                    consecutiveWordIndex.append(i)
                    wordIndex = consecutiveWordIndex
            foundPhrases.append(wordIndex)        
        else:
            if word in ii.keys(): 
                foundPhrases.append(ii[word])
        number += 1
    for el in foundPhrases:
        placeholder = []
        for i in el:
            if sceneOrPlay == "play":
                id = getPlayId(i[0],fd)
                if id not in placeholder:
                    placeholder.append(id)
            else: 
                id = getSceneId(i[0],fd)
                if id not in placeholder:
                    placeholder.append(id)
        foundScenes.append(placeholder)

    if andFlag == True:
        for tag in foundScenes:
            for i in tag:
                inAll = True
                for tag2 in foundScenes:
                    if i not in tag2:
                        inAll = False
                if inAll == True and i not in finalList:
                    finalList.append(i)               
    else: 
        for tag in foundScenes:
            for i in tag:
                finalList.append(i)  
    return finalList

def createInvertedList(fd):
    il = {}
    for i in fd:
        tokenizedWords = i["text"].split()
        place = 0
        for tokenWord in tokenizedWords:
            if tokenWord in il.keys():
                il[tokenWord].append([i["sceneNum"],place])
            else:
                il[tokenWord] = [[i["sceneNum"],place]]
            place += 1   
    return il
"""def count(fd):
    numElements= len(fd)
    totalLength = 0
    longestS = 0
    longestSName= ""
    shortestS = 1000000
    shortestSName=""
    lastPlay = ""
    playTotalLength = 0
    shortestP = 100000000
    shortestPName = ""
    longestP = 0
    longestPName= ""
    playLengths = []
    playNames = []
    for i in fd:

        tempLength = len(i["text"])
        totalLength += tempLength
        if len(i["text"]) < shortestS:
            shortestS = len(i["text"])
            shortestSName = i["sceneId"]
        if len(i["text"]) > longestS:
            longestS = len(i["text"])
            longestSName = i["sceneId"]
    for i in fd:
        
        if lastPlay == "":
            lastPlay = i["playId"]
        if lastPlay != i["playId"]:
            playLengths.append(playTotalLength)
            playNames.append(i["playId"])
            playTotalLength = 0
            lastPlay = i["playId"]
        playTotalLength += len(i["text"])
    playLengths.append(playTotalLength)
    playNames.append(i["playId"])

    for i, num in enumerate(playLengths):
        if num > longestP:
            longestP = num
            longestPName = playNames[i]
        if num < shortestP:
            shortestP = num
            shortestPName = playNames[i]

        
            

    average = (totalLength / numElements)    
    print(average,longestSName,shortestSName,longestPName,shortestPName)
"""
main()
