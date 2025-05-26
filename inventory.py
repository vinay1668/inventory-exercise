import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os

# --- Define Colors ---
PASTEL_WINDOW_BG = "#E3F2FD"
DARK_MAGENTA_BG = "#8B008B"
WHITE_TEXT = "white"
MAGENTA_TEXT = "#8B008B"
PURPLE_TEXT = "#6A0DAD"

class InventoryManager:
    def __init__(self):
        """Initialize the Inventory Manager with file paths and bottle case rules."""
        # Bottle quantity rules for case calculations
        self.bottle_case_rules = {
            "250 ml": 48,
            "500 ml": 24,
            "750 ml": 12,
            "1 lit": 12
        }
        
        # Paths for inventory files (adjust these paths according to your system)
        self.file_paths = {
            "Whisky": "References/Whisky.xlsx",
            "Vodka": "References/Vodka.xlsx",
            "Rum": "References/Rum.xlsx",
            "Zin": "References/Zin.xlsx"
        }
        
        # Create References directory if it doesn't exist
        os.makedirs("References", exist_ok=True)
        
        # Initialize Excel files if they don't exist
        self.initialize_excel_files()
    
    def initialize_excel_files(self):
        """Create Excel files with sample data if they don't exist."""
        sample_data = {
            "Whisky": {
                "Brand": ["JAMBO PREMIUM WHISKY", "PAPA 888 Whisky", "Ballantine's", "Black Dog Reserve"],
                "250 ml_Cases": [0, 0, 0, 0],
                "250 ml_Loose_Bottles": [0, 0, 0, 0],
                "500 ml_Cases": [0, 0, 0, 0],
                "500 ml_Loose_Bottles": [0, 0, 0, 0],
                "750 ml_Cases": [0, 0, 0, 0],
                "750 ml_Loose_Bottles": [0, 0, 0, 0],
                "1 lit_Cases": [0, 0, 0, 0],
                "1 lit_Loose_Bottles": [0, 0, 0, 0]
            },
            "Vodka": {
                "Brand": ["Grey Goose", "Absolut", "Belvedere", "Ketel One"],
                "250 ml_Cases": [0, 0, 0, 0],
                "250 ml_Loose_Bottles": [0, 0, 0, 0],
                "500 ml_Cases": [0, 0, 0, 0],
                "500 ml_Loose_Bottles": [0, 0, 0, 0],
                "750 ml_Cases": [0, 0, 0, 0],
                "750 ml_Loose_Bottles": [0, 0, 0, 0],
                "1 lit_Cases": [0, 0, 0, 0],
                "1 lit_Loose_Bottles": [0, 0, 0, 0]
            },
            "Rum": {
                "Brand": ["Old Monk", "Bacardi", "Captain Morgan", "Havana Club"],
                "250 ml_Cases": [0, 0, 0, 0],
                "250 ml_Loose_Bottles": [0, 0, 0, 0],
                "500 ml_Cases": [0, 0, 0, 0],
                "500 ml_Loose_Bottles": [0, 0, 0, 0],
                "750 ml_Cases": [0, 0, 0, 0],
                "750 ml_Loose_Bottles": [0, 0, 0, 0],
                "1 lit_Cases": [0, 0, 0, 0],
                "1 lit_Loose_Bottles": [0, 0, 0, 0]
            },
            "Zin": {
                "Brand": ["Saini Vineyards Zinfandel", "One Leaf Zinfandel", "1000 Stories Bourbon Barrel-Aged Zinfandel"],
                "250 ml_Cases": [0, 0, 0],
                "250 ml_Loose_Bottles": [0, 0, 0],
                "500 ml_Cases": [0, 0, 0],
                "500 ml_Loose_Bottles": [0, 0, 0],
                "750 ml_Cases": [0, 0, 0],
                "750 ml_Loose_Bottles": [0, 0, 0],
                "1 lit_Cases": [0, 0, 0],
                "1 lit_Loose_Bottles": [0, 0, 0]
            }
        }
        
        for beverage_type, data in sample_data.items():
            file_path = self.file_paths[beverage_type]
            if not os.path.exists(file_path):
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, engine="openpyxl")
                print(f"Created {file_path} with sample data")
    
    def load_brands_from_excel(self, beverage_type):
        """Load brands from the corresponding Excel file."""
        try:
            if beverage_type not in self.file_paths:
                return []
            
            file_path = self.file_paths[beverage_type]
            
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found!")
                return []
            
            df = pd.read_excel(file_path, engine="openpyxl")
            
            if "Brand" not in df.columns:
                print("Error: 'Brand' column missing in the Excel file!")
                return []
            
            return df["Brand"].tolist()
        
        except Exception as e:
            print(f"Error loading brands: {e}")
            return []
    
    def calculate_stock(self, category, bottles):
        """Calculate cases and loose bottles based on the selected category."""
        try:
            if category in self.bottle_case_rules:
                case_size = self.bottle_case_rules[category]
                cases = bottles // case_size
                loose_bottles = bottles % case_size
                return cases, loose_bottles
            else:
                print("Error: Invalid category selection.")
                return None, None
        except Exception as e:
            print(f"Error calculating stock: {e}")
            return None, None
    
    def update_stock_in_excel(self, beverage_type, brand, category, bottles, stock_type):
        """Updates the inventory in the Excel sheet based on user selection."""
        try:
            if not (beverage_type and brand and category and str(bottles).isdigit()):
                return False, "Invalid data input!"
            
            bottles = int(bottles)
            
            # Load the Excel file
            file_path = self.file_paths[beverage_type]
            df = pd.read_excel(file_path, engine="openpyxl")
            
            # Check if required columns exist
            cases_col = f"{category}_Cases"
            bottles_col = f"{category}_Loose_Bottles"
            
            if cases_col not in df.columns or bottles_col not in df.columns:
                return False, f"Columns '{cases_col}' or '{bottles_col}' are missing in the file!"
            
            # Check if brand exists
            if brand not in df["Brand"].values:
                return False, "Brand not found in inventory."
            
            # Calculate cases and loose bottles
            if stock_type == "Case (XX)":
                # If input is in cases, convert to bottles first
                total_bottles = bottles * self.bottle_case_rules[category]
                cases, loose_bottles = self.calculate_stock(category, total_bottles)
            else:  # Bottle(s)
                cases, loose_bottles = self.calculate_stock(category, bottles)
            
            # Update stock values
            df.loc[df["Brand"] == brand, cases_col] += cases
            df.loc[df["Brand"] == brand, bottles_col] += loose_bottles
            
            # Save back to Excel
            df.to_excel(file_path, index=False, engine="openpyxl")
            
            return True, f"Stock updated! {cases} cases & {loose_bottles} loose bottles added."
        
        except Exception as e:
            return False, f"Error updating stock: {e}"
    
    def get_current_stock(self, beverage_type, brand, category):
        """Get current stock for a specific brand and category."""
        try:
            file_path = self.file_paths[beverage_type]
            df = pd.read_excel(file_path, engine="openpyxl")
            
            cases_col = f"{category}_Cases"
            bottles_col = f"{category}_Loose_Bottles"
            
            if brand in df["Brand"].values:
                cases = df.loc[df["Brand"] == brand, cases_col].iloc[0]
                bottles = df.loc[df["Brand"] == brand, bottles_col].iloc[0]
                return cases, bottles
            
            return 0, 0
        
        except Exception as e:
            print(f"Error getting current stock: {e}")
            return 0, 0

class InventoryGUI:
    def __init__(self):
        """Initialize the GUI application."""
        self.inventory_manager = InventoryManager()
        self.setup_main_window()
        self.setup_variables()
        self.setup_notebook()
        self.setup_add_stock_tab()
    
    def setup_main_window(self):
        """Setup the main window."""
        self.root = tk.Tk()
        self.root.title("Stock Management System")
        self.root.geometry("1200x600")
        self.root.configure(bg=PASTEL_WINDOW_BG)
    
    def setup_variables(self):
        """Setup tkinter variables."""
        self.beverage_var = tk.StringVar()
        self.brand_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.stock_type_var = tk.StringVar()
    
    def setup_notebook(self):
        """Setup the tabbed interface."""
        self.notebook = ttk.Notebook(self.root)
        
        # Define style for tabs
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 14, "bold"), padding=[25, 15], foreground=MAGENTA_TEXT)
        style.map("TNotebook.Tab", background=[("selected", "#87CEEB"), ("!selected", "skyblue")])
        
        # Create tabs
        self.tab_open_stock = ttk.Frame(self.notebook)
        self.tab_sale_stock = ttk.Frame(self.notebook)
        self.tab_add_stock = ttk.Frame(self.notebook)
        self.tab_closing_stock = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_open_stock, text="Open Stock")
        self.notebook.add(self.tab_sale_stock, text="Sale Stock")
        self.notebook.add(self.tab_add_stock, text="Add Stock")
        self.notebook.add(self.tab_closing_stock, text="Closing Stock")
        
        self.notebook.pack(expand=True, fill="both")
    
    def setup_add_stock_tab(self):
        """Setup the Add Stock tab with all controls."""
        # Main frame for Add Stock tab
        frame_add_stock = tk.Frame(self.tab_add_stock, bg=PASTEL_WINDOW_BG)
        frame_add_stock.pack(pady=40)
        
        # Grid frame for dropdowns
        frame_grid = tk.Frame(frame_add_stock, bg=PASTEL_WINDOW_BG)
        frame_grid.pack(pady=10)
        
        # Beverage Type Dropdown
        ttk.Label(frame_grid, text="Type Of Beverage", font=("Arial", 12, "bold"), foreground=PURPLE_TEXT).grid(row=0, column=0, padx=8, pady=(5, 0), sticky="w")
        self.beverage_dropdown = ttk.Combobox(frame_grid, textvariable=self.beverage_var, values=["Whisky", "Rum", "Zin", "Vodka"], width=20, font=("Arial", 12))
        self.beverage_dropdown.grid(row=1, column=0, padx=8, pady=5)
        self.beverage_dropdown.bind("<<ComboboxSelected>>", self.update_brands)
        
        # Brand Dropdown
        ttk.Label(frame_grid, text="Brand", font=("Arial", 12, "bold"), foreground=PURPLE_TEXT).grid(row=0, column=1, padx=8, pady=(5, 0), sticky="w")
        self.brand_dropdown = ttk.Combobox(frame_grid, textvariable=self.brand_var, values=[], width=25, font=("Arial", 12))
        self.brand_dropdown.grid(row=1, column=1, padx=8, pady=5)
        
        # Category Dropdown
        ttk.Label(frame_grid, text="Category", font=("Arial", 12, "bold"), foreground=PURPLE_TEXT).grid(row=0, column=2, padx=8, pady=(5, 0), sticky="w")
        self.category_dropdown = ttk.Combobox(frame_grid, textvariable=self.category_var, values=["250 ml", "500 ml", "750 ml", "1 lit"], width=18, font=("Arial", 12))
        self.category_dropdown.grid(row=1, column=2, padx=8, pady=5)
        
        # Stock Type Dropdown
        ttk.Label(frame_grid, text="Stock Type", font=("Arial", 12, "bold"), foreground=PURPLE_TEXT).grid(row=0, column=3, padx=8, pady=(5, 0), sticky="w")
        self.stock_type_dropdown = ttk.Combobox(frame_grid, textvariable=self.stock_type_var, values=["Case (XX)", "Bottle(s)"], width=18, font=("Arial", 12))
        self.stock_type_dropdown.grid(row=1, column=3, padx=8, pady=5)
        
        # Quantity Entry
        frame_quantity = tk.Frame(frame_add_stock, bg=PASTEL_WINDOW_BG)
        frame_quantity.pack(pady=20)
        
        ttk.Label(frame_quantity, text="Quantity", font=("Arial", 12, "bold"), foreground=PURPLE_TEXT).pack()
        self.quantity_entry = tk.Entry(frame_quantity, width=24, font=("Arial", 12))
        self.quantity_entry.pack(pady=5)
        # Current Stock Display (continued)
        self.current_stock_label = tk.Label(frame_quantity, text="Current Stock: Select beverage, brand and category", font=("Arial", 10), bg=PASTEL_WINDOW_BG, fg=PURPLE_TEXT)
        self.current_stock_label.pack(pady=5)
        
        # Bind events to update current stock display
        self.brand_dropdown.bind("<<ComboboxSelected>>", self.update_current_stock)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_current_stock)
        
        # Buttons Frame
        buttons_frame = tk.Frame(self.tab_add_stock, bg=PASTEL_WINDOW_BG)
        buttons_frame.pack(pady=20)
        
        # Clear Button
        clear_btn = tk.Button(buttons_frame, text="Clear", width=12, font=("Arial", 12), 
                             bg=DARK_MAGENTA_BG, fg=WHITE_TEXT, command=self.clear_fields)
        clear_btn.pack(side="left", padx=8)
        
        # Add Button
        add_btn = tk.Button(buttons_frame, text="Add Stock", width=12, font=("Arial", 12), 
                           bg=DARK_MAGENTA_BG, fg=WHITE_TEXT, command=self.add_stock)
        add_btn.pack(side="left", padx=8)
        
        # View Stock Button
        view_btn = tk.Button(buttons_frame, text="View Stock", width=12, font=("Arial", 12), 
                            bg=DARK_MAGENTA_BG, fg=WHITE_TEXT, command=self.view_stock)
        view_btn.pack(side="left", padx=8)
    
    def update_brands(self, event=None):
        """Update brand dropdown based on selected beverage type."""
        try:
            selected_beverage = self.beverage_var.get()
            if selected_beverage:
                # Load brands from Excel file
                brands = self.inventory_manager.load_brands_from_excel(selected_beverage)
                self.brand_dropdown["values"] = brands
                self.brand_var.set("")  # Reset brand selection
                self.update_current_stock()  # Update stock display
        except Exception as e:
            messagebox.showerror("Error", f"Error updating brands: {e}")
    
    def update_current_stock(self, event=None):
        """Update current stock display."""
        try:
            beverage = self.beverage_var.get()
            brand = self.brand_var.get()
            category = self.category_var.get()
            
            if beverage and brand and category:
                cases, bottles = self.inventory_manager.get_current_stock(beverage, brand, category)
                self.current_stock_label.config(text=f"Current Stock: {cases} cases, {bottles} bottles")
            else:
                self.current_stock_label.config(text="Current Stock: Select beverage, brand and category")
        except Exception as e:
            self.current_stock_label.config(text="Error loading current stock")
    
    def clear_fields(self):
        """Clear all input fields."""
        self.beverage_var.set("")
        self.brand_var.set("")
        self.category_var.set("")
        self.stock_type_var.set("")
        self.quantity_entry.delete(0, tk.END)
        self.brand_dropdown["values"] = []
        self.current_stock_label.config(text="Current Stock: Select beverage, brand and category")
    
    def add_stock(self):
        """Add stock to inventory."""
        try:
            # Get values from form
            beverage = self.beverage_var.get()
            brand = self.brand_var.get()
            category = self.category_var.get()
            stock_type = self.stock_type_var.get()
            quantity = self.quantity_entry.get()
            
            # Validate inputs
            if not all([beverage, brand, category, stock_type, quantity]):
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Please enter a valid positive quantity!")
                return
            
            # Update stock in Excel
            success, message = self.inventory_manager.update_stock_in_excel(
                beverage, brand, category, int(quantity), stock_type
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.update_current_stock()  # Refresh current stock display
                # Optionally clear fields after successful addition
                # self.clear_fields()
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def view_stock(self):
        """View current stock in a popup window."""
        try:
            beverage = self.beverage_var.get()
            
            if not beverage:
                messagebox.showerror("Error", "Please select a beverage type first!")
                return
            
            # Create popup window
            popup = tk.Toplevel(self.root)
            popup.title(f"{beverage} Stock Overview")
            popup.geometry("800x400")
            popup.configure(bg=PASTEL_WINDOW_BG)
            
            # Create treeview for displaying stock
            columns = ("Brand", "250ml Cases", "250ml Bottles", "500ml Cases", "500ml Bottles", 
                      "750ml Cases", "750ml Bottles", "1L Cases", "1L Bottles")
            
            tree = ttk.Treeview(popup, columns=columns, show="headings", height=15)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=90)
            
            # Load data from Excel
            file_path = self.inventory_manager.file_paths[beverage]
            df = pd.read_excel(file_path, engine="openpyxl")
            
            # Insert data into treeview
            for index, row in df.iterrows():
                tree.insert("", "end", values=(
                    row["Brand"],
                    row["250 ml_Cases"], row["250 ml_Loose_Bottles"],
                    row["500 ml_Cases"], row["500 ml_Loose_Bottles"],
                    row["750 ml_Cases"], row["750 ml_Loose_Bottles"],
                    row["1 lit_Cases"], row["1 lit_Loose_Bottles"]
                ))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack widgets
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y", pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error viewing stock: {e}")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main function to run the application."""
    try:
        app = InventoryGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
        
        
