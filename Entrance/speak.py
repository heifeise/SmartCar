import os


def espaek_english(words):
    os.system('espeak ' + words)


def espeak_chinese(words):
    os.system('espeak -vzh+f2 ' + words)
