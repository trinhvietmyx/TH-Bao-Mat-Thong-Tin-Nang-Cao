class PlayFairCipher:
    def __init__(self):
        pass

    def _normalize_letters(self, text):
        return ''.join(char.upper().replace('J', 'I') for char in text if char.isalpha())

    def create_playfair_matrix(self, key):
        key = self._normalize_letters(key)
        if not key:
            raise ValueError("Key must contain at least one letter.")

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix_letters = []
        seen = set()

        for letter in key + alphabet:
            if letter not in seen:
                seen.add(letter)
                matrix_letters.append(letter)
            if len(matrix_letters) == 25:
                break

        return [matrix_letters[i:i + 5] for i in range(0, len(matrix_letters), 5)]

    def find_letter_coords(self, matrix, letter):
        letter = letter.upper().replace('J', 'I')
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Letter {letter} is not in the Playfair matrix.")

    def _prepare_plain_text(self, plain_text):
        letters = self._normalize_letters(plain_text)
        pairs = []
        index = 0

        while index < len(letters):
            first = letters[index]
            second = letters[index + 1] if index + 1 < len(letters) else "X"

            if first == second:
                pairs.append(first + "X")
                index += 1
            else:
                pairs.append(first + second)
                index += 2

        return pairs

    def playfair_encrypt(self, plain_text, matrix):
        encrypted_text = ""

        for pair in self._prepare_plain_text(plain_text):
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = self._normalize_letters(cipher_text)
        if len(cipher_text) % 2 != 0:
            cipher_text += "X"

        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i + 2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return self._remove_fillers(decrypted_text)

    def _remove_fillers(self, text):
        result = []
        index = 0

        while index < len(text):
            if (
                index + 2 < len(text)
                and text[index] == text[index + 2]
                and text[index + 1] == "X"
            ):
                result.append(text[index])
                index += 2
            else:
                result.append(text[index])
                index += 1

        if result and result[-1] == "X":
            result.pop()

        return ''.join(result)
