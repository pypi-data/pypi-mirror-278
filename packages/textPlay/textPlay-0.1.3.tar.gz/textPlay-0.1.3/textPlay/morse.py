class Morse:
    """
    A class for encoding and decoding text to/from Morse code.

    Attributes:
        morse_code_dict (dict): A dictionary mapping characters to their corresponding Morse code.

    Methods:
        coder(text)
        decoder(morse_code)
    """

    def __init__(self):
        # Define a dictionary mapping characters to Morse code
        self.morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.',
            ' ': '/'
        }


    def coder(self, text):
        """
        Encode text to Morse code.

        Args:
            text (str): The input text to be encoded.

        Returns:
            str: The encoded Morse code.
            
        Note:
            This function uses a dictionary to map characters to their corresponding
            Morse code. If the character is not found in the dictionary, it is kept
            as it is.

        Example:
        >>> morse = Morse()
        >>> encoded_text = morse.coder("Hello, World!")
        >>> print("Encoded Text:", encoded_text)

        """
        morse_code = []
        for char in text.upper():
            if char in self.morse_code_dict:
                morse_code.append(self.morse_code_dict[char])
            else:
                morse_code.append(char)  # Keep non-alphanumeric characters as they are
        return ' '.join(morse_code)


    def decoder(self, morse_code):
        """
        Decode Morse code to text.

        Args:
            morse_code (str): The input Morse code to be decoded.

        Returns:
            str: The decoded text.

        Note:
            his function uses a dictionary to map characters to their corresponding
            orse code. If the character is not found in the dictionary, it is kept
            s it is.

        Example:
        >>> morse = Morse()
        >>> decoded_text = morse.decoder(encoded_text)
        >>> print("Decoded Text:", decoded_text)
        """
        morse_dict = {value: key for key, value in self.morse_code_dict.items()}

        words = morse_code.strip().split(" / ")
        decoded_words = []

        for word in words:
            decoded_letters = []
            letters = word.split()

            for letter in letters:
                if letter in morse_dict:
                    decoded_letters.append(morse_dict[letter])
                else:
                    decoded_letters.append(letter)

            decoded_words.append("".join(decoded_letters))

        return " ".join(decoded_words)


