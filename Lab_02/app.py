import os

from flask import Flask, abort, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

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

CIPHER_CONFIGS = {
    "caesar": {
        "title": "Caesar Cipher",
        "label": "Caesar",
        "key_type": "number",
        "plain_sample": "HUTECH",
        "cipher_sample": "MZYJMR",
        "key_sample": "5",
    },
    "vigenere": {
        "title": "Vigenere Cipher",
        "label": "Vigenere",
        "key_type": "text",
        "plain_sample": "HUTECH",
        "cipher_sample": "HVVEDJ",
        "key_sample": "ABC",
    },
    "railfence": {
        "title": "Rail Fence Cipher",
        "label": "Rail Fence",
        "key_type": "number",
        "plain_sample": "HUTECHUNIVERSITY",
        "cipher_sample": "HCISUEHNVRITYUET",
        "key_sample": "3",
    },
    "playfair": {
        "title": "Playfair Cipher",
        "label": "Playfair",
        "key_type": "text",
        "plain_sample": "HOMNAYHANHDONG",
        "cipher_sample": "FHOANBBOOYHRYQ",
        "key_sample": "MONARCHY",
    },
    "transposition": {
        "title": "Transposition Cipher",
        "label": "Transposition",
        "key_type": "number",
        "plain_sample": "HUTECH",
        "cipher_sample": "HEUCTH",
        "key_sample": "3",
    },
}


@app.context_processor
def inject_menu():
    return {"cipher_configs": CIPHER_CONFIGS}


def _numeric_key(key):
    try:
        return int(key)
    except (TypeError, ValueError) as exc:
        raise ValueError("Key must be a number.") from exc


def _encrypt(cipher_name, text, key):
    if cipher_name == "caesar":
        return caesar_cipher.encrypt_text(text, _numeric_key(key)), None
    if cipher_name == "vigenere":
        return vigenere_cipher.vigenere_encrypt(text, key), None
    if cipher_name == "railfence":
        return railfence_cipher.rail_fence_encrypt(text, _numeric_key(key)), None
    if cipher_name == "playfair":
        matrix = playfair_cipher.create_playfair_matrix(key)
        return playfair_cipher.playfair_encrypt(text, matrix), matrix
    if cipher_name == "transposition":
        return transposition_cipher.encrypt(text, _numeric_key(key)), None
    raise ValueError("Unsupported cipher.")


def _decrypt(cipher_name, text, key):
    if cipher_name == "caesar":
        return caesar_cipher.decrypt_text(text, _numeric_key(key)), None
    if cipher_name == "vigenere":
        return vigenere_cipher.vigenere_decrypt(text, key), None
    if cipher_name == "railfence":
        return railfence_cipher.rail_fence_decrypt(text, _numeric_key(key)), None
    if cipher_name == "playfair":
        matrix = playfair_cipher.create_playfair_matrix(key)
        return playfair_cipher.playfair_decrypt(text, matrix), matrix
    if cipher_name == "transposition":
        return transposition_cipher.decrypt(text, _numeric_key(key)), None
    raise ValueError("Unsupported cipher.")


def _render_cipher(cipher_name, result=None, error=None):
    config = CIPHER_CONFIGS.get(cipher_name)
    if config is None:
        abort(404)
    return render_template(
        f"{cipher_name}.html",
        cipher_name=cipher_name,
        config=config,
        result=result,
        error=error,
    )


def _form_value(*names):
    for name in names:
        value = request.form.get(name)
        if value:
            return value
    return ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


@app.route("/<cipher_name>")
def cipher_page(cipher_name):
    return _render_cipher(cipher_name)


@app.route("/rail-fence")
def rail_fence_page():
    return redirect(url_for("cipher_page", cipher_name="railfence"))


@app.post("/<cipher_name>/encrypt")
def cipher_encrypt(cipher_name):
    text = _form_value("inputPlainText", "input_text")
    key = _form_value("inputKeyPlain", "input_key")
    try:
        output, matrix = _encrypt(cipher_name, text, key)
        return _render_cipher(
            cipher_name,
            result={
                "mode": "Encryption",
                "input_label": "Plain text",
                "output_label": "Encrypted text",
                "text": text,
                "key": key,
                "output": output,
                "matrix": matrix,
            },
        )
    except ValueError as exc:
        return _render_cipher(cipher_name, error=str(exc))


@app.post("/<cipher_name>/decrypt")
def cipher_decrypt(cipher_name):
    text = _form_value("inputCipherText", "input_text")
    key = _form_value("inputKeyCipher", "input_key")
    try:
        output, matrix = _decrypt(cipher_name, text, key)
        return _render_cipher(
            cipher_name,
            result={
                "mode": "Decryption",
                "input_label": "Cipher text",
                "output_label": "Decrypted text",
                "text": text,
                "key": key,
                "output": output,
                "matrix": matrix,
            },
        )
    except ValueError as exc:
        return _render_cipher(cipher_name, error=str(exc))


@app.post("/encrypt")
def caesar_encrypt_legacy():
    return cipher_encrypt("caesar")


@app.post("/decrypt")
def caesar_decrypt_legacy():
    return cipher_decrypt("caesar")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
