# 🧁 Cupcake

**Expense tracker that makes budgeting as easy as eating a cupcake.**  
Cupcake is a lightweight Flask app to help you manage your money, track your expenses, and stay within budget — all stored locally using JSON files. No database setup, just simple and sweet.

---

## 🍰 Features

- 🔐 User Authentication (Login/Signup)
- 💸 Add, View, and Delete Expenses
- 📅 Track Monthly Budgets
- 🗂️ Category-wise Spending Limits
- 📊 Dashboard with Summaries
- 💾 JSON-based Local Storage

---

## 🗂️ Project Structure
```
cupcake/
├── app.py # Main Flask app
├── static/
│ └── style.css # CSS styles
├── templates/
│ ├── index.html # Login page
│ ├── dashboard.html # Expense dashboard
│ ├── budget.html # Budget interface
├── data/
│ ├── users.json # User accounts
│ ├── transactions.json # Expense records
│ └── budgets.json # Budget data
└── utils/
└── json_utils.py # JSON file read/write helpers
```


---

## 🧠 JSON Format Samples

### `users.json`
```json
[
  {
    "id": 1,
    "username": "alice",
    "password": "hashed_password"
  }
]
```


### `transactions.json`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "amount": 50.0,
    "category": "Groceries",
    "date": "2025-05-18",
    "note": "Weekly veggies"
  }
]
```
### `budgets.json`
```json
[
  {
    "user_id": 1,
    "monthly_limit": 500.0,
    "categories": {
      "Groceries": 200.0,
      "Transport": 100.0
    }
  }
]
```

🛠️ Getting Started
Clone the repo

git clone https://github.com/yourusername/cupcake.git
cd cupcake


Install dependencies

pip install Flask


Run the app

python app.py


Open your browser and go to http://localhost:5000


