import cs50


def main():
    card_number = int(card_input())
    check_card(card_number)


def card_input():
    '''This is a function to prompt user for card number.

    If card number is not an integer,
    user will be reprompted until an acceptable number is entered.'''
    while True:
        n = cs50.get_int('Enter card number: ')
        return n


def invalid():
    print('INVALID')


def luhn_check(number):
    s = str(number)
    s = s[::-1]  # reverse card number
    length = len(s)
    x = 0
    y = 0
    # count through every other digit in card number string starting from second to last number,
    # multiply odd by 2, add each result's digit, add the rest of card digits
    for i in range(length):
        if i % 2 != 0:
            current = int(s[i]) * 2
            a = str(current)
            for m in range(len(a)):
                x += int(a[m])
        else:
            y += int(s[i])
    z = x + y
    luhn = z % 10  # if mod 10 of the sum is 0, then tha card is valid, return true
    if luhn == 0:
        return True
    else:
        return False


def check_card(number):  # function to check if card is valid
    s = str(number)
    length = len(s)  # get length
    if (length < 13) or (length > 16) or (luhn_check(number) != True):
        invalid()
    elif (int(s[0]) == 3) and (int(s[1]) == 4 or int(s[1]) == 7) and (length == 15):
        print('AMEX')
    elif (int(s[0]) == 5) and (int(s[1]) in range(1, 6)) and (length == 16):
        print('MASTERCARD')
    elif (int(s[0]) == 4) and (length == 13 or length == 16):
        print('VISA')


main()
