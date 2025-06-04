import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import numpy as np

class CropDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Yield Data Analysis")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10), width=100, height=30)
        self.text_area.pack(padx=10, pady=10)

        self.load_btn = tk.Button(root, text="Analyze Crop Data", command=self.load_csv, bg="#007acc", fg="white", padx=10, pady=5)
        self.load_btn.pack(pady=5)

    def load_csv(self):
        file_path = "crop_yield.csv"  # 📌 Put your CSV file name here

        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()

            output = []

            output.append("🔹 First 5 rows:\n")
            output.append(df.head().to_string(index=False) + "\n\n")

            output.append(f"🔹 Shape of dataset: {df.shape}\n\n")

            output.append("🔹 Summary statistics:\n")
            output.append(df.describe().to_string() + "\n\n")

            output.append("🔹 Missing values per column:\n")
            output.append(df.isnull().sum().to_string() + "\n\n")

            cat_cols = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition', 'Fertilizer_Used', 'Irrigation_Used']
            for col in cat_cols:
                if col in df.columns:
                    output.append(f"🔹 Unique values in {col}: {df[col].unique().tolist()}\n")
            output.append("\n")

            if 'Crop' in df.columns and 'Yield_tons_per_hectare' in df.columns:
                avg_yield_crop = df.groupby("Crop")["Yield_tons_per_hectare"].mean().sort_values(ascending=False)
                output.append("🔹 Average yield per crop:\n")
                output.append(avg_yield_crop.to_string() + "\n\n")

            if 'Region' in df.columns and 'Crop' in df.columns:
                crop_count_region = df.groupby("Region")["Crop"].count()
                output.append("🔹 Number of crops grown in each region:\n")
                output.append(crop_count_region.to_string() + "\n\n")

            if 'Region' in df.columns and 'Yield_tons_per_hectare' in df.columns:
                avg_yield_region = df.groupby("Region")["Yield_tons_per_hectare"].mean()
                output.append("🔹 Average crop yield by region:\n")
                output.append(avg_yield_region.to_string() + "\n\n")

            output.append("🔹 Correlation matrix (numerical features):\n")
            output.append(df.corr(numeric_only=True).to_string() + "\n")

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "\n".join(output))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CropDataApp(root)
    root.mainloop()
