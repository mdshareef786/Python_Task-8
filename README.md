# 💰 Smart Expense Manager

> A real-time **Expense Tracking & Financial Analysis System** built using Python and MySQL.
> Designed with clean architecture, OOP principles, and functional programming to simulate a production-grade application.

---

## 🎯 Objective

Build a smart system to:

* Track daily expenses
* Categorize spending
* Analyze financial behavior
* Generate meaningful insights for better money management

---

## 🌍 Real-Time Use Case

This application can be used for:

* Personal finance tracking
* Budget planning
* Monthly expense analysis
* Identifying overspending patterns

---

## 🚀 Key Highlights

* ✅ OOP-based architecture (Encapsulation, Inheritance, Abstraction)
* ✅ Functional programming using `map()`, `filter()`, `reduce()`
* ✅ MySQL database integration (real-time storage)
* ✅ Smart Insights
* ✅ Category-wise and monthly reports
* ✅ Fully interactive CLI application
* ✅ CRUD operations (Create, Read, Update, Delete)

---

## 🛠️ Tech Stack

| Layer     | Technology                   |
| --------- | ---------------------------- |
| Language  | Python 3.10+                 |
| Database  | MySQL 8.0                    |
| Connector | mysql-connector-python       |
| Concepts  | OOP · Functional Programming |
| Interface | Command Line (CLI)           |

---

## 🗄️ Database Schema

```sql
CREATE DATABASE IF NOT EXISTS expense_db;
USE expense_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE expenses (
    exp_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(100),
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Optional View
CREATE VIEW expenses_view AS
SELECT exp_id, user_id, amount, category, description, date FROM expenses;
```

---

## 🧠 OOP Architecture

```
AbstractBase (ABC)
│
└── User (Encapsulation)
    │
    └── Expense (Inheritance + Method Overriding)
```

### Concepts Implemented

* **Encapsulation** → Private variables (`__amount`, `__category`)
* **Inheritance** → `Expense` extends `User`
* **Abstraction** → Abstract base class
* **Polymorphism** → Method overriding (`toString()`, `toDict()`)
* **super()** → Used for parent initialization

---

## ⚙️ Functional Programming

| Function                 | Usage                                |
| ------------------------ | ------------------------------------ |
| `filter()`               | Filter by category & date            |
| `map()`                  | Extract expense amounts              |
| `reduce()`               | Total, highest, monthly calculations |
| Dictionary Comprehension | Category-wise spending               |

---

## 📊 Features

### 👤 User Management

* Add new user
* View all users

### 💸 Expense Management

* Add expense
* View user expenses
* Update expense
* Delete expense

### 🔍 Filtering

* Filter by category
* Filter by date range

### 📈 Reports & Analysis

#### 1. Total Spending

* Calculates total using `map()` + `reduce()`

#### 2. Category-wise Spending

```
Food: ₹2000
Travel: ₹1500
Shopping: ₹3000
```

#### 3. Monthly Report

* Aggregates expenses month-wise

#### 4. Highest Expense

* Identified using `reduce()`

---

## 🧠 Smart Insights (Advanced Logic)

Example Output:

```
TOTAL SPENT: ₹12,500
TOP CATEGORY: Food (47%)
⚠ Warning: You are spending heavily on Food!
```

👉 Triggers alert when:

* Any category exceeds **40% of total spending**

---

## 📋 Application Menu

```
1. Add User
2. View Users
3. Add Expense
4. View Expenses
5. Filter by Category
6. Filter by Date
7. Total Spending
8. Category Report
9. Monthly Report
10. Highest Expense
11. Update Expense
12. Delete Expense
13. Smart Insights
0. Exit
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install mysql-connector-python
```

### 2. Setup database

* Run SQL script in MySQL

### 3. Configure DB connection

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="expense_db"
    )
```

### 4. Run application

```bash
python main.py
```

---

## 📁 Project Structure

```
smart-expense-manager/
│
├── main.py
└── README.md
```

---

## 💡 Sample Output

```
ID    Amount    Category     Date
----------------------------------------
1     ₹2000     Food         2025-06-01
2     ₹1500     Travel       2025-06-03

TOTAL SPENT: ₹3500
TOP CATEGORY: Food (57%)
⚠ Warning: You are spending heavily on Food!
```

---

## 👨‍💻 Developer

**Syed Mahammad Shareef** | Python Developer

---

## 🔥 Future Enhancements

* Build REST API using FastAPI
* Add UI using Streamlit / React
* Add authentication system
* Deploy on cloud (AWS / Render)

---

## 📄 License

This project is licensed under the MIT License.
