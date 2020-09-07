from cs50 import get_string
import sys


def main():
    # prompt for text:
    t = get_string("Text: ")
    # get length of text entered:
    length = len(t)
    grade = calculate(t, length)
    # results printing with conditions
    if (1 < grade < 16):
        print(f'Grade {grade}')
    elif (grade >= 16):
        print(f'Grade 16+')
    else:
        print('Before Grade 1')


def calculate(t, length):
    # initializing a list with lowercase letters
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    words = 0
    letters = 0
    sentences = 0
    t = t.lower()
    # calculation of words, letters, sentences
    if t[0] in alphabet:
        words = 1  # first word
    for i in range(length):
        if t[i] in alphabet:
            letters += 1  # letters counter
        if (i < (length - 1)) and (t[i] == ' ') and (t[i + 1] in alphabet):
            words += 1  # words counter
    special = list('.!?')
    for a in range(length):  # sentenses counter
        if (t[a] in special) and (t[a - 1] in alphabet):
            sentences += 1
        elif (t[a] == '"') and (t[a - 1] == '?' or t[a - 1] == '!') and (t[a - 2] in alphabet):
            sentences += 1
    # grade calculation:
    s = (sentences / words) * 100.0
    l = (letters / words) * 100.0
    g = (0.0588 * l) - (0.296 * s) - 15.8
    grade = round(g)  # final grade rounded from float
    return grade


main()
