class VigenereCipher:
    def __init__(self):
        pass

    def _clean_key(self, key):
        cleaned_key = ''.join(char.upper() for char in key if char.isalpha())
        if not cleaned_key:
            raise ValueError("Key must contain at least one letter.")
        return cleaned_key

    def vigenere_encrypt(self, plain_text, key):
        key = self._clean_key(key)
        encrypted_text = ""
        key_index = 0

        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                encrypted_text += chr((ord(char) - base + key_shift) % 26 + base)
                key_index += 1
            else:
                encrypted_text += char

        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        key = self._clean_key(key)
        decrypted_text = ""
        key_index = 0

        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                decrypted_text += chr((ord(char) - base - key_shift) % 26 + base)
                key_index += 1
            else:
                decrypted_text += char

        return decrypted_text
