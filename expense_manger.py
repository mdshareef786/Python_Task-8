import mysql.connector
from abc import ABC, abstractmethod
from functools import reduce
from datetime import date

# DATABASE CONNECTION

def get_connection():
    return mysql.connector.connect(
        host     = "localhost",
        user     = "root",
        password = "1911",
        database = "expense_db"
    )

# ABSTRACT BASE CLASS

class AbstractBase(ABC):
    @abstractmethod
    def toString(self) -> str:
        pass

    @abstractmethod
    def toDict(self) -> dict:
        pass

# USER CLASS — Encapsulation

class User(AbstractBase):
    def __init__(self, user_id: int, name: str, email: str = ""):
        self.__user_id = user_id   # private variable
        self.__name    = name      # private variable
        self.__email   = email     # private variable

    def get_id(self)    -> int:  return self.__user_id
    def get_name(self)  -> str:  return self.__name
    def get_email(self) -> str:  return self.__email

    def toString(self) -> str:
        return f"[User #{self.__user_id}: {self.__name}]"

    def toDict(self) -> dict:
        return {"user_id": self.__user_id, "name": self.__name, "email": self.__email}

    @staticmethod
    def create(name: str, email: str = "") -> "User":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f" User created: {name} (ID: {user_id})")
        return User(user_id, name, email)

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [User(r["user_id"], r["name"], r.get("email","")) for r in rows]

    @staticmethod
    def get_by_id(user_id: int) -> "User | None":
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        return User(r["user_id"], r["name"], r.get("email","")) if r else None

# EXPENSE CLASS — Inheritance & Method Overriding

class Expense(User):
    def __init__(self, exp_id: int, user_id: int, user_name: str,
                 amount: float, category: str, description: str, exp_date: str):
        super().__init__(user_id, user_name) 
        self.__exp_id      = exp_id
        self.__amount      = float(amount)  
        self.__category    = category   
        self.__description = description 
        self.__date        = exp_date 

    def get_exp_id(self)      -> int:   return self.__exp_id
    def get_amount(self)      -> float: return self.__amount
    def get_category(self)    -> str:   return self.__category
    def get_description(self) -> str:   return self.__description
    def get_date(self)        -> str:   return str(self.__date)

    def toString(self) -> str:
        return (f"[Expense #{self.__exp_id}] ₹{self.__amount:.0f} | {self.__category} | {self.__date}")

    def toDict(self) -> dict:
        return {"exp_id": self.__exp_id, "user_id": self.get_id(), "amount": self.__amount, "category": self.__category, "date": str(self.__date)}

    @staticmethod
    def add(user_id: int, amount: float, category: str, description: str, exp_date: str) -> "Expense":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, amount, category, description, exp_date))
        conn.commit()
        exp_id = cursor.lastrowid
        cursor.close()
        conn.close()
        user = User.get_by_id(user_id)
        print(f" Expense added: ₹{amount}")
        return Expense(exp_id, user_id, user.get_name(), amount, category, description, exp_date)

    @staticmethod
    def get_all_expenses() -> list:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT e.*, u.name AS user_name FROM expenses e JOIN users u ON e.user_id = u.user_id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Expense(r["exp_id"], r["user_id"], r["user_name"], r["amount"], r["category"], r["description"], str(r["date"])) for r in rows]

    @staticmethod
    def get_all_for_user(user_id: int) -> list:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT e.*, u.name AS user_name FROM expenses e JOIN users u ON e.user_id = u.user_id WHERE e.user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Expense(r["exp_id"], r["user_id"], r["user_name"], r["amount"], r["category"], r["description"], str(r["date"])) for r in rows]

    @staticmethod
    def update(exp_id: int, amount: float, category: str, description: str, exp_date: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET amount=%s, category=%s, description=%s, date=%s WHERE exp_id=%s", (amount, category, description, exp_date, exp_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(exp_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE exp_id = %s", (exp_id,))
        conn.commit()
        cursor.close()
        conn.close()

# FUNCTIONAL LOGIC (Filter, Map, Reduce)

def filter_by_category(expenses: list, category: str) -> list:
    return list(filter(lambda e: e.get_category().lower() == category.lower(), expenses))

def filter_by_date(expenses: list, from_date: str, to_date: str) -> list:
    return list(filter(lambda e: from_date <= e.get_date() <= to_date, expenses))

def total_expense(expenses: list) -> float:
    if not expenses: return 0.0
    amounts = list(map(lambda e: e.get_amount(), expenses)) 
    return reduce(lambda a, b: a + b, amounts) 

def highest_expense(expenses: list):
    if not expenses: return None
    return reduce(lambda a, b: a if a.get_amount() > b.get_amount() else b, expenses)

def category_spending(expenses: list) -> dict:
    categories = {e.get_category() for e in expenses} 
    return {cat: sum(e.get_amount() for e in expenses if e.get_category() == cat) for cat in categories}

def monthly_report(expenses: list) -> dict:
    def reducer(acc, e):
        month = e.get_date()[:7]
        acc[month] = acc.get(month, 0) + e.get_amount()
        return acc
    return reduce(reducer, expenses, {})

# SMART INSIGHTS & DISPLAY

def smart_insights(expenses: list):
    if not expenses:
        print(" No expenses found.")
        return
    total = total_expense(expenses)
    cat_dict = category_spending(expenses)
    top_cat = max(cat_dict, key=cat_dict.get)
    top_pct = round(cat_dict[top_cat] / total * 100, 1)
    
    print(f"\n TOTAL SPENT: ₹{total:,.0f}")
    print(f" TOP CATEGORY: {top_cat} ({top_pct}%)")
    if top_pct > 40:
        print(f" Warning: You are spending heavily on {top_cat}!")
    else:
        print(" Spending is well-balanced.")

def print_expenses(expenses: list):
    if not expenses:
        print(" No data to display.")
        return
    print(f"{'ID':<5} {'Amount':>8}  {'Category':<12} {'Date'}")
    print("-" * 40)
    for e in expenses:
        print(f"{e.get_exp_id():<5} ₹{e.get_amount():>7,.0f}  {e.get_category():<12} {e.get_date()}")

# MAIN MENU

def main():
    while True:
        print("\n" + "="*30 + "\n SMART EXPENSE MANAGER \n" + "="*30)
        print("1. Add User\n2. View Users\n3. Add Expense\n4. View Expenses\n5. Filter by Category")
        print("6. Filter by Date\n7. Total Spending\n8. Category Report\n9. Monthly Report\n10. Highest Expense")
        print("11. Update Expense\n12. Delete Expense\n13. Smart Insights\n0. Exit")
        
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            name, email = input("Name: "), input("Email: ")
            User.create(name, email)

        elif choice == "2":
            for u in User.get_all(): print(u.toString())

        elif choice == "3":
            uid = int(input("User ID: "))
            amt = float(input("Amount: "))
            cats = ["Food", "Travel", "Shopping", "Health", "Other"]
            print("Categories:", " | ".join(f"{i+1}.{c}" for i,c in enumerate(cats)))
            while True:
                try:
                    ci = int(input("Choose (1-5): ")) - 1
                    if 0 <= ci < len(cats):
                        cat = cats[ci]
                        break
                    else:
                        print(" Please choose between 1 and 5.")
                except ValueError:
                    print(" Enter a number between 1 and 5.")
            desc = input("Description: ")
            dt = input("Date (YYYY-MM-DD) or enter for today: ") or str(date.today())
            Expense.add(uid, amt, cat, desc, dt)

        elif choice == "4":
            uid = int(input("User ID: "))
            print_expenses(Expense.get_all_for_user(uid))

        elif choice == "5":
            cat = input("Enter Category: ")
            print_expenses(filter_by_category(Expense.get_all_expenses(), cat))
        
        elif choice == "6":
            start = input("Start (YYYY-MM-DD): ")
            end = input("End (YYYY-MM-DD): ")
            print_expenses(filter_by_date(Expense.get_all_expenses(), start, end))

        elif choice == "7":
            uid = int(input("User ID: "))
            print(f"Total: ₹{total_expense(Expense.get_all_for_user(uid)):,.2f}")
        
        elif choice == "8":
            report = category_spending(Expense.get_all_expenses())
            for c, a in report.items(): print(f"{c}: ₹{a:,.2f}")

        elif choice == "9":
            uid = int(input("User ID: "))
            report = monthly_report(Expense.get_all_for_user(uid))
            for m, t in report.items(): print(f"{m}: ₹{t:,.2f}")

        elif choice == "10":
            high = highest_expense(Expense.get_all_expenses())
            if high: print(high.toString())
        
        elif choice == "11":
            print("\n" + "-"*30 + "\n UPDATE EXPENSE \n" + "-"*30)
            all_records = Expense.get_all_expenses()
            
            if not all_records:
                print(" No expenses found in the system.")
            else:
                print_expenses(all_records)
                eid = int(input("\n Enter the Expense ID you want to update: "))
                
                if any(e.get_exp_id() == eid for e in all_records):
                    amt = float(input(" New Amount: ₹"))
                    
                    cats = ["Food", "Travel", "Shopping", "Health", "Other"]
                    print(" Choose New Category:", " | ".join(f"{i+1}.{c}" for i,c in enumerate(cats)))
                    while True:
                        try:
                            ci = int(input(" Selection (1-5): ")) - 1
                            if 0 <= ci < len(cats):
                                cat = cats[ci]
                                break
                            else: print(" Choose 1-5.")
                        except ValueError: print(" Enter a number.")
                    
                    desc = input(" New Description: ")
                    dt = input(" New Date (YYYY-MM-DD): ") or str(date.today())
                    
                    Expense.update(eid, amt, cat, desc, dt)
                    print(f" Expense #{eid} updated successfully.")
                else:
                    print(f" Error: ID #{eid} not found.")

        elif choice == "12":
            print("\n" + "-"*30 + "\n DELETE EXPENSE \n" + "-"*30)
            all_records = Expense.get_all_expenses()
            
            if not all_records:
                print(" No expenses found to delete.")
            else:
                print_expenses(all_records)
                eid = int(input("\n Enter the Expense ID you want to DELETE: "))
                
                if any(e.get_exp_id() == eid for e in all_records):
                    confirm = input(f" Are you sure you want to delete ID #{eid}? (y/n): ").lower()
                    if confirm == 'y':
                        Expense.delete(eid)
                        print(f" Expense #{eid} removed from database.")
                    else:
                        print(" Delete cancelled.")
                else:
                    print(f" Error: ID #{eid} not found.")

        elif choice == "13":
            uid = int(input("User ID: "))
            smart_insights(Expense.get_all_for_user(uid))

        elif choice == "0":
            print("Thank You!"); break

if __name__ == "__main__":
    main()


