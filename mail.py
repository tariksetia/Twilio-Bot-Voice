import random
def generateRandomPassword():
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    digit = '012345678'
    schar = '!@#$%^&*'

    passowrd = ''

    for i in range(3):
        passowrd += random.choice(upper)
    
    for i in range(4):
        passowrd += random.choice(lower)

    passowrd += random.choice(schar)

    for i in range(4):
        passowrd += random.choice(digit)

    return passowrd


if __name__ == '__main__':
    for i in range(10):
        print(generateRandomPassword())