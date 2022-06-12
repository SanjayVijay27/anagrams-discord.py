dictionary = open("collins_scrabble_words.txt")
dictionary1 = dictionary.read()
dictionary2 = dictionary1[59:-1]
anagramsDict = []
s = ""
for i in dictionary2:
    if i != "n" and i != '\n':
        s = s + i
    elif i == "\n":
        anagramsDict.append(s)
        s = ""

def anagram(board, length):
    words = []
    for i in anagramsDict:
        if len(i) <= len(board.upper()) and len(i) >= length:
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    words.append(i)
    return words

def anagramExact(board, length):
    words = []
    for i in anagramsDict:
        if len(i) <= len(board.upper()) and len(i) == length:
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    words.append(i)
    return words

def anagramFirst(board):
    word = ""
    broke = False
    for i in anagramsDict:
        if len(i) <= len(board.upper()) and len(i) == len(board):
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    word = i
                    broke = True
        if broke:
            break
    return word

def anagramSort(board):
    summary = ""
    for i in range(3, len(board)):
        summary += "\n" + str(i) + ": "
        anas = anagram(board, 3)
        for j in anas:
            if len(j) == i:
                summary += j + ", "
    return summary

def findCombo(board, length):
    words = []
    for i in anagramsDict:
        if len(i) <= len(board.upper()) - 1 and len(i) == length:
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    if anagramFirst(i) not in words:
                        words.append(i)
    return words

def anaScoreFull(board):
    score = 0
    anas = anagram(board, 3)
    for word in anas:
        if len(word) == 3:
            score += 100
        elif len(word) == 4:
            score += 400
        elif len(word) == 5:
            score += 1200
        elif len(word) == 6:
            score += 2000
        elif len(word) == 7:
            score += 3000
    return score

def anaScore6(board):
    score = 0
    anas = anagram(board, 5)
    for word in anas:
        if len(word) == 5:
            score += 1200
        elif len(word) == 6:
            score += 2000
    return score

def anaScore7(board):
    score = 0
    anas = anagram(board, 6)
    for word in anas:
        if len(word) == 6:
            score += 2000
        elif len(word) == 7:
            score += 3000
    return score

from dotenv import load_dotenv
import os

load_dotenv()

import discord
client = discord.Client()

@client.event
async def on_ready():
    print("Successfully logged in as " + str(client.user))

@client.event
async def on_message(message):
    mList = message.content.split()
    if message.author == client.user:
        return
    
    if mList[0] == "!ana":
        if mList[1].upper() == "COMBO":
            if len(anagram(mList[2], len(mList[2]))) == 0:
                await message.channel.send("That word has no valid anagrams.")
            else:
                await message.channel.send(anagram(mList[2], len(mList[2])))
                if anagram(mList[2], len(mList[2]))[0] == "UNALERTED":
                    await message.channel.send("NUTDEALER\nshhhhhhhh")

        elif mList[1].upper() == "FULLSCORE":
            await message.channel.send(str(anaScoreFull(mList[2]) / 1000.0) + "k")
        
        elif mList[1].upper() == "6SCORE":
            if len(mList[2]) == 6:
                await message.channel.send(str(anaScore6(mList[2]) / 1000.0) + "k")
            else:
                await message.channel.send("That word is not 6 letters long.")
        
        elif mList[1].upper() == "7SCORE":
            if len(mList[2]) == 7:
                await message.channel.send(str(anaScore7(mList[2]) / 1000.0) + "k")
            else:
                await message.channel.send("That word is not 7 letters long.")
        
        elif mList[1].upper() == "ALLWORDS":
            string = "Remember to expand the file to see every word\n"
            for i in range(3, len(mList[2]) + 1):
                anas = anagramExact(mList[2], i)
                string += str(i) + " letter words: \n"
                if len(anas) == 0:
                    string += "None\n"
                else:
                    string += str(anas) + "\n\n"
            outputNewFile = open('output.txt', 'w')
            outputNewFile.write(string)
            outputNewFile.close()
            await message.channel.send(file = discord.File("output.txt"))
            outputNewFile = open("output.txt","r+")
            outputNewFile.truncate(0)
            outputNewFile.close()
        
        elif mList[1].upper() == "ALLCOMBOS":
            string = "Remember to expand the file to see every combo\n"
            for i in range(3, len(mList[2])):
                anas = findCombo(mList[2], i)
                string += str(i) + " letter combos: \n"
                if len(anas) == 0:
                    string += "None\n"
                else:
                    string += str(anas) + "\n\n"
            outputNewFile = open('output.txt', 'w')
            outputNewFile.write(string)
            outputNewFile.close()
            await message.channel.send(file = discord.File("output.txt"))
            outputNewFile = open("output.txt","r+")
            outputNewFile.truncate(0)
            outputNewFile.close()
        
        elif mList[1].upper() == "HELP":
            await message.channel.send("***!ana [command] [word]***"
            + "\n**combo**: displays all perfect anagrams of a word"
            + "\n**fullScore**: displays the maximum score of a board in Game Pigeon Anagrams"
            + "\n**6Score**: displays the maximum score of a 6-letter board using only 5s and 6s"
            + "\n**7Score**: displays the maximum score of a 7-letter board using only 6s and 7s"
            + "\n**allWords**: displays every valid word that can be made from a word"
            + "\n**allCombos**: displays every combo that exists in a word, excluding the word's own combo")

client.run(os.getenv("TOKEN"))
