from .alphabet import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        encrypted_text = []
        for letter in text:
            if not letter.isalpha():
                encrypted_text.append(letter)
                continue
            letter_index = self.alphabet.index(letter.upper())
            output_index = (letter_index + key) % alphabet_len
            output_letter = self.alphabet[output_index]
            encrypted_text.append(output_letter)
        return ''.join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        decrypted_text = []
        for letter in text:
            if not letter.isalpha():
                decrypted_text.append(letter)
                continue
            letter_index = self.alphabet.index(letter.upper())
            output_index = (letter_index - key) % alphabet_len
            output_letter = self.alphabet[output_index]
            decrypted_text.append(output_letter)
        return ''.join(decrypted_text)
