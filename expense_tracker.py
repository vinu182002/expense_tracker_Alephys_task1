# i have been imported few modules 
import json
import argparse
from datetime import datetime
from collections import defaultdict

DATE_FORMAT = "%Y-%m-%d"

# where load_data function is been  created. which can load the json file data. and my json file name is filename
def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    for item in data:
        if not all(k in item for k in ("date", "type", "amount", "category")):
            raise ValueError("Missing field in data")
    return data

# here a new function is created save_data which can save the data. 
def save_data(records, filename):
    
    with open(filename, 'w') as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} records to {filename}")

# here a new function is created get_date which can get the date from user.and if you enter the data you should enter in YYYY-MM-DD format.
def get_date():
    # Ask for a date or default to today
    s = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not s:
        return datetime.today().strftime(DATE_FORMAT)
    # here it is going to  check that the format is right
    datetime.strptime(s, DATE_FORMAT)
    return s

# here a new function is created add_entry .
# here it asks to enter the income/expense.
# and it also asks to enter the amount, date, category and note.
def add_entry():
    while True:
        t = input("Type (income/expense): ").strip().lower()
        if t in ("income", "expense"):
            break
        print("Please type 'income' or 'expense'")

    # here it is going to ask the amount and you should enter particular amount.
    amt = float(input("Amount: ").strip())
    #  now it Ask for when it happened.
    date_str = get_date()
    #  now it asks for a simple category
    cat = input("Category (e.g. Salary, Food): ").strip()
    # now it will also ask a short note if you want then you can give .if no then leave it blank
    note = input("Note (optional): ").strip()

    return {"date": date_str, "type": t, "amount": amt, "category": cat, "note": note}

# here a new function is created  show_summary  which can show the summary of the records. 
def show_summary(records):
    by_month = defaultdict(list)
    for r in records:
        month = r["date"][0:7]
        by_month[month].append(r)

    if not by_month:
        print("No data to show.")
        return

    # Print each month in order with totals
    for month in sorted(by_month):
        income = sum(r["amount"] for r in by_month[month] if r["type"] == "income")
        expense = sum(r["amount"] for r in by_month[month] if r["type"] == "expense")
        net = income - expense
        print(f"\nMonth: {month}")
        print(f"  Income : {income}")
        print(f"  Expense: {expense}")
        print(f"  Net    : {net}")

        #  and the next step is to Show expense breakdown by category 
        cat_totals = defaultdict(float)
        for r in by_month[month]:
            if r["type"] == "expense":
                cat_totals[r["category"]] += r["amount"]
        if cat_totals:
            print("  By Category:")
            for cat, tot in cat_totals.items():
                print(f"    {cat}: {tot}")


def show_menu():
    print("""
1) Add entry
2) Show summary
3) Save to file
4) Load from file
5) Quit
""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="load data from JSON file")
    args = parser.parse_args()

    # Start with an empty list or load from a file
    records = []
    if args.file:
        try:
            records = load_data(args.file)
            print(f"Loaded {len(records)} records from {args.file}")
        except Exception as e:
            print("Error loading file:", e)

    # note: this is the  Main loop
    while True:
        show_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            rec = add_entry()
            records.append(rec)
            print("Entry added.")
        elif choice == "2":
            show_summary(records)
        elif choice == "3":
            fn = input("Filename to save: ").strip()
            save_data(records, fn)
        elif choice == "4":
            fn = input("Filename to load: ").strip()
            try:
                more = load_data(fn)
                records.extend(more)
                print(f"Loaded {len(more)} more records.")
            except Exception as e:
                print("Error:", e)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please enter a number 1-5.")


if __name__ == "__main__":
    main()
