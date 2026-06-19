from flask import Flask, jsonify, request

from cipher.caesar import CaesarCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()


def _json_data():
    return request.get_json(silent=True) or {}


def _int_value(data, key_name):
    try:
        return int(data[key_name])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{key_name} must be an integer.") from exc


def _required_text(data, key_name):
    value = data.get(key_name)
    if value is None:
        raise ValueError(f"{key_name} is required.")
    return str(value)


def _error_response(error):
    return jsonify({"error": str(error)}), 400


# CAESAR CIPHER ALGORITHM
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    try:
        data = _json_data()
        plain_text = _required_text(data, "plain_text")
        key = _int_value(data, "key")
        encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
        return jsonify({
            "encrypted_message": encrypted_text,
            "encrypted_text": encrypted_text,
        })
    except ValueError as error:
        return _error_response(error)


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    try:
        data = _json_data()
        cipher_text = _required_text(data, "cipher_text")
        key = _int_value(data, "key")
        decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
        return jsonify({
            "decrypted_message": decrypted_text,
            "decrypted_text": decrypted_text,
        })
    except ValueError as error:
        return _error_response(error)


# VIGENERE CIPHER ALGORITHM
@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    try:
        data = _json_data()
        plain_text = _required_text(data, "plain_text")
        key = _required_text(data, "key")
        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as error:
        return _error_response(error)


@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    try:
        data = _json_data()
        cipher_text = _required_text(data, "cipher_text")
        key = _required_text(data, "key")
        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as error:
        return _error_response(error)


# RAILFENCE CIPHER ALGORITHM
@app.route("/api/railfence/encrypt", methods=["POST"])
@app.route("/api/rail-fence/encrypt", methods=["POST"])
def railfence_encrypt():
    try:
        data = _json_data()
        plain_text = _required_text(data, "plain_text")
        key = _int_value(data, "key")
        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as error:
        return _error_response(error)


@app.route("/api/railfence/decrypt", methods=["POST"])
@app.route("/api/rail-fence/decrypt", methods=["POST"])
def railfence_decrypt():
    try:
        data = _json_data()
        cipher_text = _required_text(data, "cipher_text")
        key = _int_value(data, "key")
        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as error:
        return _error_response(error)


# PLAYFAIR CIPHER ALGORITHM
@app.route("/api/playfair/creatematrix", methods=["POST"])
def playfair_creatematrix():
    try:
        data = _json_data()
        key = _required_text(data, "key")
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        return jsonify({"playfair_matrix": playfair_matrix})
    except ValueError as error:
        return _error_response(error)


@app.route("/api/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    try:
        data = _json_data()
        plain_text = _required_text(data, "plain_text")
        key = _required_text(data, "key")
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as error:
        return _error_response(error)


@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    try:
        data = _json_data()
        cipher_text = _required_text(data, "cipher_text")
        key = _required_text(data, "key")
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as error:
        return _error_response(error)


# TRANSPOSITION CIPHER ALGORITHM
@app.route("/api/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    try:
        data = _json_data()
        plain_text = _required_text(data, "plain_text")
        key = _int_value(data, "key")
        encrypted_text = transposition_cipher.encrypt(plain_text, key)
        return jsonify({"encrypted_text": encrypted_text})
    except ValueError as error:
        return _error_response(error)


@app.route("/api/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    try:
        data = _json_data()
        cipher_text = _required_text(data, "cipher_text")
        key = _int_value(data, "key")
        decrypted_text = transposition_cipher.decrypt(cipher_text, key)
        return jsonify({"decrypted_text": decrypted_text})
    except ValueError as error:
        return _error_response(error)


# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
