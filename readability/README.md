# Readability

### Overview

'Readability' is a program that computes the approximate grade level needed to comprehend some text.<br>
It uses the Coleman-Liau index that is computed as 
> index = 0.0588 * L - 0.296 * S - 15.8  

where L is the average number of letters per 100 words in the text, and S is the average number of sentences per 100 words in the text.<br>
The bigger the index, the higher the complexity.

### Usage

Run the program as follows:
> $ python readability.py

The program will prompt the user for some excerpt of text to be analyzed:
> Text: A large class of computational problems involve the determination of properties of graphs, digraphs, integers, arrays of integers, finite families of finite sets, boolean formulas and elements of other countable domains.

The output:
> Grade 16+

