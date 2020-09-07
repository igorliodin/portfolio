# DNA

### Overview

'DNA' is a command line Python program that identifies a person based on their DNA patterns (sequences of nucleotides).

### Usage

Below is an example of program's usage.<br>
CSV file provided contains STR counts for a list of individuals, sequence file contains a DNA sequence to be inspected.
> $ python dna.py databases/large.csv sequences/5.txt

Output:
> Lavender

### Background

DNA is a sequence of molecules called nucleotides, arranged into a particular shape (a double helix).<br> 
Each nucleotide of DNA contains one of four different bases: adenine (A), cytosine (C), guanine (G), or thymine (T).<br>
One place where DNA tends to have high genetic diversity is in Short Tandem Repeats (STRs).<br>
An STR is a short sequence of DNA bases that tends to repeat consecutively numerous times at specific locations inside of a person’s DNA. <br>
The number of times any particular STR repeats varies a lot among individuals.<br>
If two DNA samples match in the number of repeats for each of the STRs, the analyst can be pretty confident they came from the same person.<br>

### How it works

The program does the following:<br>

- Open the CSV file and read its contents into memory
- Open the DNA sequence and read its contents into memory
- For each of the STRs (from the first line of the CSV file), compute the longest run of consecutive repeats of the STR in the DNA sequence to identify
- If the STR counts match exactly with any of the individuals in the CSV file, print out the name of the matching individual
- If the STR counts do not match exactly with any of the individuals in the CSV file, print "No match"
