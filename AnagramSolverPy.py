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

dictionary = open("combo_words.txt")
dictionary1 = dictionary.read()
comboDict = []
s = ""
for i in dictionary1:
    if i != "n" and i != '\n':
        s = s + i
    elif i == "\n":
        comboDict.append(s)
        s = ""

def formatScore(num):
    if num < 1000:
        score = str(num)
    elif num < 1000000:
        score = str(num / 1000.0) + "k"
    elif num < 1000000000:
        score = str(num / 1000000.0) + "M"
    else:
        score = "a really big number (this shouldn't even happen; contact speedster#0012 if it does)"
    return score

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
    for i in comboDict:
        if len(i) == len(board):
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    word = i
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
    words = {}
    for i in comboDict:
        if len(i) == length:
            wordCopy = list(i)
            boardCopy = list(board.upper())
            while len(wordCopy) > 0 and wordCopy[0] in boardCopy:
                commonLetter = wordCopy[0]
                wordCopy.remove(commonLetter)
                boardCopy.remove(commonLetter)
                if len(wordCopy) == 0:
                    words[i] = len(anagramExact(i, len(i)))
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
bot = discord.Bot()

@bot.event
async def on_ready():
    print("Successfully logged in as " + str(bot.user))

@bot.command(name="combo", description="displays all perfect anagrams of a word")
async def combo(ctx, word):
    if len(anagram(word, len(word))) == 0:
        await ctx.respond("That word has no valid anagrams.")
    else:
        await ctx.respond(anagram(word, len(word)))

@bot.command(name="full_score", description="displays the maximum score of a board in Game Pigeon Anagrams")
async def full_score(ctx, word):
    await ctx.respond(formatScore(anaScoreFull(word)))

@bot.command(name="six_score", description="displays the maximum score of a 6-letter board using only 5s and 6s")
async def six_score(ctx, word):
    if len(word) == 6:
        await ctx.respond(formatScore(anaScore6(word)))
    else:
        await ctx.respond("That word is not 6 letters long.")

@bot.command(name="seven_score", description="displays the maximum score of a 7-letter board using only 5s and 6s")
async def seven_score(ctx, word):
    if len(word) == 7:
        await ctx.respond(formatScore(anaScore7(word)))
    else:
        await ctx.respond("That word is not 7 letters long.")

@bot.command(name="all_words", description="displays every valid word that can be made from a word")
async def all_words(ctx, word):
    string = "Remember to expand the file to see more\nYou may have to download the file if it is too large for Discord to fully display\n"
    for i in range(3, len(word) + 1):
        anas = anagramExact(word, i)
        string += str(i) + " letter words: \n"
        if len(anas) == 0:
            string += "None\n"
        else:
            string += str(anas) + "\n\n"
    outputNewFile = open('output.txt', 'w')
    outputNewFile.write(string)
    outputNewFile.close()
    await ctx.respond(file = discord.File("output.txt"))
    outputNewFile = open("output.txt","r+")
    outputNewFile.truncate(0)
    outputNewFile.close()

@bot.command(name="all_combos", description="displays every combo that exists in a word with their word counts, excluding the word's own combo")
async def all_combos(ctx, word):
    string = "Remember to expand the file to see more\nYou may have to download the file if it is too large for Discord to fully display\n"
    for i in range(3, len(word)):
        anas = findCombo(word, i)
        string += str(i) + " letter combos: \n"
        if len(anas) == 0:
            string += "None\n"
        else:
            string += str(anas) + "\n\n"
    outputNewFile = open('output.txt', 'w')
    outputNewFile.write(string)
    outputNewFile.close()
    await ctx.respond(file = discord.File("output.txt"))
    outputNewFile = open("output.txt","r+")
    outputNewFile.truncate(0)
    outputNewFile.close()

@bot.command(name="help", description="displays every command and their descriptions")
async def help(ctx):
    await ctx.respond("***Use as Discord Slash Commands***"
        + "\n**combo**: displays all perfect anagrams of a word"
        + "\n**full_score**: displays the maximum score of a board in Game Pigeon Anagrams"
        + "\n**six_score**: displays the maximum score of a 6-letter board using only 5s and 6s"
        + "\n**seven_score**: displays the maximum score of a 7-letter board using only 6s and 7s"
        + "\n**all_words**: displays every valid word that can be made from a word"
        + "\n**all_combos**: displays every combo that exists in a word with their word counts, excluding the word's own combo")

bot.run(os.getenv("TOKEN"))