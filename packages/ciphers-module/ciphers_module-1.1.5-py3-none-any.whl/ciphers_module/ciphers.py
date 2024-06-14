from itertools import islice, cycle

def get_letter_value(letter: str) -> int:
    '''Get the value of an English letter (A = 0, B = 1, C = 2 ...)'''
    return ord(letter) - 65

def get_letter_from_value(value: int) -> str:
    '''Get the English letter from a value (A = 0, B = 1, C = 2 ...)'''
    return chr(value + 65)

def caeser_cipher(text: str, shift: int, decode: bool = False) -> str:
    '''
    Caeser Cipher\n
    Shifts {text} {shift} amount in positive/negative direction (Right/Left respectively)\n
    Set {decode} to True to decode {text} with shift {shift}
    '''
    # Make everything Upper Case
    text.upper()

    # Begin
    result: str = ""
    for letter in text:
        # Get Value of each Letter
        value: int = get_letter_value(letter)
        # Get Letter from Value
        result += get_letter_from_value(value + shift) if not decode else get_letter_from_value(value - shift) # Handle Decoding

    return result

def vigenere_cipher(text: str, key: str, decode: bool = False) -> str:
    '''
    Vigenere Cipher\n
    Uses a Vigenere Cipher on {text} with key {key}\n
    Set {decode} to True to decode {text} with key {key}
    '''
    # Make everything Upper Case
    text.upper()
    key.upper()

    # Make Lists of Characters
    text_lst: list[str] = list(text)
    key_lst: list[str] = list(key)

    # Edit Length of Key
    if len(key_lst) < len(text_lst):
        key_lst = list(islice(cycle(key_lst), len(text_lst)))
    if len(key_lst) > len(text_lst):
        key_lst = key_lst[:len(key_lst)]

    result: str = ""

    for index, letter in enumerate(text_lst):
        # Get Values of each Letter
        letter_value: int = get_letter_value(letter)
        key_value: int = get_letter_value(key_lst[index]) if not decode else -get_letter_value(key_lst[index]) # Handle Decoding
        # Get Letter from Value
        new_letter: str = get_letter_from_value((letter_value + key_value) % 26)
        result += new_letter

    return result

def rail_fence_cipher(text: str, rails: int, decode: bool = False):
    '''
    Rail Fence Cipher\n
    Uses a Rail Fence (Zig-Zag) Cipher on {text} with {rails} rails\n
    Set {decode} to True to decode {text} with {rails} rails
    '''
    # Make everything Upper Case
    text.upper()
    
    # Make Rail Fence
    rail_fence = [[""]*len(text) for _ in range(rails)]

    # Variables to move the cursor
    direction = -1
    row = 0

    if decode:  # Decoding
        # Fill the rail_fence with placeholders
        for col in range(len(text)):
            rail_fence[row][col] = '*'

            # Change direction if we've hit the top or bottom rail
            if row == 0 or row == rails - 1:
                direction *= -1

            # Move to the next row
            row += direction

        # Fill the rail rail_fence with the ciphertext
        i = 0
        for row in range(rails):
            for col in range(len(text)):
                if rail_fence[row][col] == '*':
                    rail_fence[row][col] = text[i]
                    i += 1

        # Extract the plaintext from the rail_fence
        result = [rail_fence[row][col] for col in range(len(text)) for row in range(rails) if rail_fence[row][col] is not None]

    else:  # Encoding
        # Fill the rail rail_fence
        for col in range(len(text)):
            rail_fence[row][col] = text[col]

            # Change direction if we've hit the top or bottom rail
            if row == 0 or row == rails - 1:
                direction *= -1

            # Move to the next row
            row += direction

        # Extract the text from the rail_fence
        result = [rail_fence[row][col] for row in range(rails) for col in range(len(text)) if rail_fence[row][col] is not None]

    return "".join(result)

class ascii:
    '''
    Class for doing ASCII encoding and decoding on text in multiple formats.
    '''

    @staticmethod
    def decimal(text: str, decode: bool = False) -> str:
        '''
        ASCII Decimal\n
        Converts a string to and from decimal using ASCII
        '''
        result: str = ""
        if not decode:
            for letter in text:
                value: str = str(ord(letter))
                result += f"{value} "
            return result
        for number in text.split():
            try:
                value = chr(int(number))
                result += value
            except ValueError:
                print("Not a number")
        return result

    @staticmethod
    def binary(text: str, decode: bool = False) -> str:
        '''
        ASCII Binary\n
        Converts a string to and from binary using ASCII
        '''
        result: str = ""
        if not decode:
            for letter in text:
                value: str = bin(ord(letter)).removeprefix("0b")
                result += f"0{value} "
            return result
        for byte in text.split():
            try:
                value = chr(int(byte, 2))
                result += value
            except ValueError:
                print(f"Not Binary: {byte}")
        return result
    
    @staticmethod
    def octal(text: str, decode: bool = False) -> str:
        '''
        ASCII Hexadecimal\n
        Converts a string to and from hexadecimal using ASCII
        '''
        result: str = ""
        if not decode:
            for letter in text:
                value: str = oct(ord(letter)).removeprefix("0o")
                result += f"{value} "
            return result
        for octa in text.split():
            try:
                value = chr(int(octa, 8))
                result += value
            except ValueError:
                print(f"Not Octal: {octa}")
        return result

    @staticmethod
    def hexadecimal(text: str, decode: bool = False) -> str:
        '''
        ASCII Hexadecimal\n
        Converts a string to and from hexadecimal using ASCII
        '''
        result: str = ""
        if not decode:
            for letter in text:
                value: str = hex(ord(letter)).removeprefix("0x")
                result += f"{value} "
            return result
        for hexa in text.split():
            try:
                value = chr(int(hexa, 16))
                result += value
            except ValueError:
                print(f"Not Hexadecimal: {hexa}")
        return result

# Testing
if __name__ == '__main__':
    print(f"Caeser Cipher (Shift: 3→)\nEncoding: {caeser_cipher("HELLO", 3)}")
    print(f"Decoding: {caeser_cipher("KHOOR", 3, True)}\n")

    print(f"Vigenere Cipher (Key: 'KEY')\nEncoding: {vigenere_cipher('HELLO', 'KEY')}")
    print(f"Decoding: {vigenere_cipher('RIJVS', 'KEY', True)}\n")
    
    print(f"Rail Fence Cipher (Key: 'KEY')\nEncoding: {rail_fence_cipher('HELLO', 3)}")
    print(f"Decoding: {rail_fence_cipher('HOELL', 3, True)}\n")

    print(f"ASCII Binary\nEncoding: {ascii.binary("HELLO")}")
    print(f"Decoding: {ascii.binary("01001000 01000101 01001100 01001100 01001111", True)}\n")

    print(f"ASCII Decimal\nEncoding: {ascii.decimal("HELLO")}")
    print(f"Decoding: {ascii.decimal("72 69 76 76 79", True)}\n")

    print(f"ASCII Hexadimal\nEncoding: {ascii.hexadecimal("HELLO")}")
    print(f"Decoding: {ascii.hexadecimal("48 45 4c 4c 4f", True)}\n")

    print(f"ASCII Octal\nEncoding: {ascii.octal("HELLO")}")
    print(f"Decoding: {ascii.octal("01001000 01000101 01001100 01001100 01001111", True)}\n")