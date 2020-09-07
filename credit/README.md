#Credit

### Overview

'Credit' is a command line program written in Python that determines whether a provided credit card number is valid according to Luhn’s algorithm

### About Luhn's algorithm

Luhn's algorithm works the following way:
1. Multiply every other digit by 2, starting with the number’s second-to-last digit, and then add those products’ digits together.
2. Add the sum to the sum of the digits that weren’t multiplied by 2.
3. If the total’s last digit is 0 (or, put more formally, if the total modulo 10 is congruent to 0), the number is valid!

More info here: [Wikipedia](https://en.wikipedia.org/wiki/Luhn_algorithm)

### Usage

$ python credit.py

The program will prompt for a credit card number to check.
A valid number should result in a credit card type: Visa, MasterCard or AMEX.
An invalid number results in a corresponding message: "INVALID"
