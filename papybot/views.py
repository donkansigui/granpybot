from flask import Flask, render_template, request, jsonify



@app.route("/")
def index():
    return render_template('index.html')