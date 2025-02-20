from flask import Flask, send_from_directory, request, jsonify
import random
import os

app = Flask(__name__, static_folder="static")

lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num, highest_num)
guesses = 0

# Főoldal kiszolgálása
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Számkitalálós játék API végpontja
@app.route('/guess', methods=['POST'])
def guess_number():
    global answer, guesses
    data = request.json
    user_guess = int(data.get("guess", 0))
    guesses += 1

    if user_guess < lowest_num or user_guess > highest_num:
        return jsonify({"message": "Ez a szám nincs a megadott tartományban!", "status": "out_of_range"})
    elif user_guess < answer:
        return jsonify({"message": "Túl alacsony! Próbáld újra.", "status": "low"})
    elif user_guess > answer:
        return jsonify({"message": "Túl magas! Próbáld újra.", "status": "high"})
    else:
        response = {
            "message": f"Gratulálok! A szám {answer} volt.",
            "status": "correct",
            "attempts": guesses
        }
        answer = random.randint(lowest_num, highest_num)  # Új szám generálása a következő játékhoz
        guesses = 0
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
