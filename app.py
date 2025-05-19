from flask import Flask, render_template, request, redirect, session, url_for, flash
from utils.json_utils import read_json, write_json
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cupcake_secret_key'

# Paths to JSON data
USER_FILE = 'data/users.json'
TRANSACTION_FILE = 'data/transactions.json'
BUDGET_FILE = 'data/budgets.json'

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = read_json(USER_FILE)
    username = request.form['username']
    password = request.form['password']

    for user in users:
        if user['username'] == username and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect('/dashboard')
    flash('Invalid credentials')
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    users = read_json(USER_FILE)
    username = request.form['username']
    password = request.form['password']

    if any(u['username'] == username for u in users):
        flash('Username already exists')
        return redirect('/')

    user_id = max([u['id'] for u in users], default=0) + 1
    new_user = {
        "id": user_id,
        "username": username,
        "password": generate_password_hash(password)
    }
    users.append(new_user)
    write_json(USER_FILE, users)
    flash('Signup successful. Please login.')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    transactions = read_json(TRANSACTION_FILE)
    user_txns = [t for t in transactions if t['user_id'] == session['user_id']]
    total = sum(t['amount'] for t in user_txns)
    return render_template('dashboard.html', transactions=user_txns, total=total)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect('/')
    
    transactions = read_json(TRANSACTION_FILE)
    txn_id = max([t['id'] for t in transactions], default=0) + 1
    new_txn = {
        "id": txn_id,
        "user_id": session['user_id'],
        "amount": float(request.form['amount']),
        "category": request.form['category'],
        "date": datetime.now().strftime('%Y-%m-%d'),
        "note": request.form['note']
    }
    transactions.append(new_txn)
    write_json(TRANSACTION_FILE, transactions)
    return redirect('/dashboard')

@app.route('/budget')
def budget():
    if 'user_id' not in session:
        return redirect('/')
    
    budgets = read_json(BUDGET_FILE)
    user_budget = next((b for b in budgets if b['user_id'] == session['user_id']), None)
    return render_template('budget.html', budget=user_budget)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect('/')
    
    budgets = read_json(BUDGET_FILE)
    user_budget = next((b for b in budgets if b['user_id'] == session['user_id']), None)
    
    new_budget = {
        "user_id": session['user_id'],
        "monthly_limit": float(request.form['monthly_limit']),
        "categories": {
            "Groceries": float(request.form.get('groceries', 0)),
            "Transport": float(request.form.get('transport', 0)),
            "Others": float(request.form.get('others', 0))
        }
    }

    if user_budget:
        budgets = [b if b['user_id'] != session['user_id'] else new_budget for b in budgets]
    else:
        budgets.append(new_budget)

    write_json(BUDGET_FILE, budgets)
    return redirect('/budget')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    for file in [USER_FILE, TRANSACTION_FILE, BUDGET_FILE]:
        if not os.path.exists(file):
            write_json(file, [])
    app.run(debug=True)
