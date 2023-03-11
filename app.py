import requests
import json
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/form_login', methods=['POST'])
def login():
    url = 'https://api.paywithextend.com/signin'
    email = request.form['email']
    password = request.form['password']
    headers = { 
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.paywithextend.v2021-03-12+json'
    }
    data = {
        'email': email,
        'password': password
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the response is successful
    if response.status_code == 200:
        auth_token = response.json()['token']
        return redirect(url_for('display_virtual_cards', auth_token=auth_token))
    else:
        # If the response is unsuccessful, reattempt login
        return render_template('fail.html')


@app.route('/virtual_cards')
def display_virtual_cards():
    url = 'https://api.paywithextend.com/virtualcards'
    auth_token = request.args.get('auth_token')
    token = 'Bearer ' + auth_token
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.paywithextend.v2021-03-12+json'
    }

    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        virtual_cards = response.json()['virtualCards']
        return render_template('index.html', virtual_cards=virtual_cards, auth_token=auth_token)
    else:
        # If the response is unsuccessful, please login
        return render_template('fail.html')


@app.route('/card_transactions/<card_id>')
def display_card_transactions(card_id):
    url = 'https://api.paywithextend.com/virtualcards/' + card_id + '/transactions'
    auth_token = request.args.get('auth_token')
    token = 'Bearer ' + auth_token
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.paywithextend.v2021-03-12+json'
    }

    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        transactions = response.json()['transactions']
        return render_template('transactions.html', transactions=transactions)
    else:
        # If the response is unsuccessful, please login
        return render_template('fail.html')
