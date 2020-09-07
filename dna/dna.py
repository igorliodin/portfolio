from sys import argv, exit
import csv


def main():
    if len(argv) != 3:                          # check for correct arguments input
        print('Usage: python dna.py data.csv sequence.txt')
        exit(1)

    with open(argv[1], 'r') as db:
        dna = csv.DictReader(db)                # using DictReader to open csv DB
        fields = list(dna.fieldnames)           # getting the list of field names
        sequence = open_text(fields)            # calling the fuction to open text file, getting the sequence
        found = False                           # a switch for finding match
        for row in dna:                         # iterating through each row in DB, comparing to sequence
            true_counter = 0                    # counter for the number of field matches
            for i in range(len(fields) - 1):    # iterating through each value in a row
                x = str(fields[i + 1])          # field name
                y = int(sequence[i])            # value from txt sequence array
                a = int(row[x])                 # corresponding field value from DB
                if a == y:                      # condition for calculating the number of matches within a row
                    true_counter += 1           # adding to a number of matches
            if true_counter == len(sequence):   # if the number of matches equals to the number of fields,
                found = True                    # switch found to true
                print(row['name'])              # print the name
                break                           # stop iterating through DB rows
        if found == False:                      # if the found switch is false after iterating through DB,
            print('No match')                   # print 'No match'


def open_text(params):                          # function for opening text file, creating array of field values
    with open(argv[2], 'r') as txt:
        x = str(txt.read())                     # x represents the contents of text file in string format
        y = []                                  # initializing array for parameters
        y = params                              # adding parameters to array
        z = []                                  # initializing array for parameter values to be further returned
        for j in range(1, len(y)):              # iterating through the string, calculations, adding to z[]
            max_count = 0
            for i in range(len(x)):
                tmp_count = 0
                a = y[j]
                while a == x[i: i + (len(a))]:
                    tmp_count += 1
                    i += len(a)
                if max_count < tmp_count:
                    max_count = tmp_count
            z.append(max_count)
        return z


main()
