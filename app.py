from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)