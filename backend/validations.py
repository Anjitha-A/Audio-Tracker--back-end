from flask import jsonify
import re

def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search("[!@#$%^&*()_+=-]", password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+=-)"
    return True, "Password is strong"

def validateRegisterData(fullname, username, password):
    if not fullname:
        return jsonify({"error": "Full name is required"}), 400
    if len(fullname) < 3:
        return jsonify({"error": "Full name must be at least 3 characters"}), 400
    if not all(i.isalpha() or i.isspace() for i in fullname):
        return jsonify({"error": "Full name can only contain letters and spaces"}), 400
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    password_is_strong, password_error = validate_password_strength(password)
    if not password_is_strong:
        return jsonify({"error": password_error}), 400
    return None
def validateLoginData( username, password):
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

def validateAudioData(title, artist, category , album, image):
    if not title:
        return jsonify({"error": "title is required"}), 400
    if not artist:
        return jsonify({"error": "artist is required"}), 400
    if not category:
        return jsonify({"error": "category is required"}), 400
    if not album:
        return jsonify({"error": "album is required"}), 400
    if not image:
        return jsonify({"error": "image is required"}), 400
    