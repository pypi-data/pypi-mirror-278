# letter_writer/app.py

from flask import Flask, request, jsonify, send_file
import socket
import sys
import logging
from letter_writer.writer import LetterByLetterWriter

app = Flask(__name__)

writer = LetterByLetterWriter()
ip_address = socket.gethostbyname(socket.gethostname())

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def print_start_message():
    print("***********************************************************")
    print("* Point the Cursor where you want to start writing from.. *")
    print("*        Do not move the cursor while writing             *")
    print(f"*             IP address: {ip_address}                   *")
    print("***********************************************************")

@app.route('/start_writing', methods=['POST'])
def start_writing():
    data = request.get_json()
    text = data['text']
    writer.start_writing(text)
    return jsonify({"message": "Writing started"})

@app.route('/stop_writing', methods=['GET'])
def stop_writing():
    writer.stop_writing()
    return jsonify({"message": "Writing stopped"})

@app.route('/take_screenshot', methods=['GET'])
def take_screenshot():
    try:
        screenshot_file = writer.take_screenshot()
        return send_file(screenshot_file, mimetype='image/png')
    except Exception as e:
        logging.error("Error taking screenshot", exc_info=True)
        return jsonify({"error": str(e)}), 500 

def main():
    print_start_message()
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")

if __name__ == "__main__":
    sys.stdout = open('app.log', 'w')
    sys.stderr = open('app.log', 'a')
    main()
