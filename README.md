# expense_tracker_Alephys_task1

This is a simple Python script to manage JSON data files. It can load and validate records from a file, and save new or updated records back.

## Features

- Load records from a JSON file
- Check that all required fields are present
- Save updated records to a file
- Useful for managing expenses or categorized data

## How It Works

### 1. Load Data
```python
from main import load_data

records = load_data('data.json')
This will read data.json and make sure every item has:

date

type

amount

category

If anything is missing, it raises an error

### 2. Save Data

from main import save_data

save_data(records, 'data.json')
This saves your list of records back to the file in readable JSON format.

