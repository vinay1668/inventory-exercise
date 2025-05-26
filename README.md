# Inventory Management System

A comprehensive GUI-based inventory management system built with Python Tkinter for managing beverage stock across multiple categories and brands.

## Features

- **Multi-beverage Support**: Manage inventory for Whisky, Vodka, Rum, and Zin
- **Dynamic Brand Loading**: Brands are loaded dynamically from Excel files based on beverage selection
- **Case/Bottle Management**: Automatic conversion between cases and individual bottles
- **Real-time Stock Display**: View current stock levels while adding new inventory
- **Excel Integration**: All data is stored and managed in Excel files
- **User-friendly GUI**: Clean, intuitive interface with tabbed navigation

## Requirements

- Python 3.7+
- pandas
- openpyxl
- tkinter (usually comes with Python)

## Installation

1. **Clone or download the project files**

2. **Install required packages:**

   ```bash
   pip install pandas openpyxl
   ```

3. **For macOS users with tkinter issues:**
   ```bash
   brew install python-tk
   ```

## Project Structure

```
inventory-management/
│
├── inventory.py          # Main application file
├── README.md            # This file
└── References/          # Excel files directory (auto-created)
    ├── Whisky.xlsx
    ├── Vodka.xlsx
    ├── Rum.xlsx
    └── Zin.xlsx
```

## How to Run

```bash
python inventory.py
```

## Usage Guide

### 1. Starting the Application

When you first run the application, it will automatically:

- Create a `References` folder
- Generate Excel files for each beverage type with sample brands
- Initialize all stock values to zero

### 2. Adding Stock

1. **Select Beverage Type**: Choose from Whisky, Vodka, Rum, or Zin
2. **Select Brand**: Brands will automatically populate based on your beverage selection
3. **Choose Category**: Select bottle size (250ml, 500ml, 750ml, 1L)
4. **Select Stock Type**: Choose whether you're adding cases or individual bottles
5. **Enter Quantity**: Input the number of cases or bottles
6. **View Current Stock**: The system shows current stock levels for the selected combination
7. **Click "Add Stock"**: Confirm the addition to update the Excel file

### 3. Viewing Stock

- Click "View Stock" to see a comprehensive overview of all brands and categories for the selected beverage type
- The view displays both cases and individual bottles for each size category

### 4. Clearing Fields

- Use the "Clear" button to reset all form fields

## Technical Details

### Case Calculation Rules

The system uses the following conversion rules:

- **250ml**: 48 bottles per case
- **500ml**: 24 bottles per case
- **750ml**: 12 bottles per case
- **1 Liter**: 12 bottles per case

### Excel File Structure

Each beverage type has its own Excel file with the following columns:

- `Brand`: Brand name
- `[Size]_Cases`: Number of cases for each size
- `[Size]_Loose_Bottles`: Number of individual bottles for each size

Example columns for Whisky.xlsx:

```
Brand | 250 ml_Cases | 250 ml_Loose_Bottles | 500 ml_Cases | 500 ml_Loose_Bottles | ...
```

### Data Flow

1. **GUI Selection** → **Excel File Reading** → **Brand Population**
2. **User Input** → **Validation** → **Case/Bottle Calculation** → **Excel Update**
3. **Stock Display** → **Real-time Excel Reading** → **Current Stock Display**

## Code Architecture

### Classes

#### `InventoryManager`

- Handles all Excel file operations
- Manages stock calculations
- Provides data validation
- Methods:
  - `load_brands_from_excel()`: Loads brands from Excel files
  - `update_stock_in_excel()`: Updates stock in Excel files
  - `calculate_stock()`: Converts bottles to cases and loose bottles
  - `get_current_stock()`: Retrieves current stock levels

#### `InventoryGUI`

- Manages the user interface
- Handles user interactions
- Connects GUI events to inventory operations
- Methods:
  - `update_brands()`: Updates brand dropdown based on beverage selection
  - `add_stock()`: Processes stock addition
  - `view_stock()`: Displays stock overview
  - `clear_fields()`: Resets form fields

### Key Features Implementation

#### Dynamic Brand Loading

```python
def update_brands(self, event=None):
    selected_beverage = self.beverage_var.get()
    brands = self.inventory_manager.load_brands_from_excel(selected_beverage)
    self.brand_dropdown["values"] = brands
```

#### Stock Calculation

```python
def calculate_stock(self, category, bottles):
    case_size = self.bottle_case_rules[category]
    cases = bottles // case_size
    loose_bottles = bottles % case_size
    return cases, loose_bottles
```

#### Excel Integration

```python
def update_stock_in_excel(self, beverage_type, brand, category, bottles, stock_type):
    df = pd.read_excel(file_path, engine="openpyxl")
    # Update calculations
    df.loc[df["Brand"] == brand, cases_col] += cases
    df.to_excel(file_path, index=False, engine="openpyxl")
```

## Customization

### Adding New Beverages

1. Add the beverage type to the dropdown values in `setup_add_stock_tab()`
2. Add the file path to `self.file_paths` in `InventoryManager.__init__()`
3. Add sample data to `sample_data` in `initialize_excel_files()`

### Modifying Case Rules

Update the `bottle_case_rules` dictionary in `InventoryManager.__init__()`:

```python
self.bottle_case_rules = {
    "250 ml": 48,  # Modify these values
    "500 ml": 24,
    # Add new sizes here
}
```

### Adding New Brands

Simply add brands directly to the Excel files, or modify the sample data in the `initialize_excel_files()` method.

## Error Handling

The application includes comprehensive error handling for:

- Missing Excel files (auto-creation)
- Invalid data input (validation)
- File read/write errors (try-catch blocks)
- Missing columns (column validation)
- Network/permission issues (graceful degradation)

## Troubleshooting

### Common Issues

1. **tkinter not found (macOS)**:

   ```bash
   brew install python-tk
   ```

2. **Excel files not found**:

   - The application auto-creates files on first run
   - Ensure write permissions in the project directory

3. **Brands not loading**:

   - Check if Excel files exist in the References folder
   - Verify the "Brand" column exists in Excel files

4. **Stock not updating**:
   - Ensure all fields are filled before clicking "Add Stock"
   - Check file permissions for Excel files

### Debug Mode

To enable debug output, uncomment print statements in the code or add:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- Add sale stock functionality
- Implement stock alerts for low inventory
- Add data export/import features
- Include barcode scanning support
- Add user authentication
- Implement database backend option

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
