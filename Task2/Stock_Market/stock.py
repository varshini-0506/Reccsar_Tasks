import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

class NetflixSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Stock & Sentiment Correlation")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2f")  # Dark background

        # Title Label
        tk.Label(
            root,
            text="📊 Netflix Stock vs Sentiment Analysis",
            font=("Helvetica", 20, "bold"),
            fg="#ffffff",
            bg="#1e1e2f"
        ).pack(pady=20)

        # Container Frame
        frame = tk.Frame(root, bg="#1e1e2f")
        frame.pack(pady=10)

        self.process_btn = tk.Button(
            frame,
            text="Process and Plot",
            command=self.process_data,
            font=("Arial", 12, "bold"),
            bg="#3a86ff",
            fg="white",
            padx=15,
            pady=8,
            relief="raised",
            bd=3,
            cursor="hand2"
        )
        self.process_btn.pack(pady=10)

        self.corr_label = tk.Label(
            root,
            text="",
            font=("Arial", 14),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        self.corr_label.pack(pady=10)

        self.stock_df = None
        self.sentiment_df = None

        # Load the files directly
        self.load_data()

    def load_data(self):
        try:
            # Load stock data
            self.stock_df = pd.read_csv("NFLX.csv")
            self.stock_df['Date'] = pd.to_datetime(self.stock_df['Date'])
            self.stock_df.set_index('Date', inplace=True)

            # Load sentiment data
            df = pd.read_csv("FAANG_STOCK_NEWS.csv")
            df = df[df['ticker'] == 'NFLX']
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
            df['date'] = pd.to_datetime(df['datetime'].dt.date)
            self.sentiment_df = df

            messagebox.showinfo("Success", "Data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")

    def process_data(self):
        try:
            daily_sentiment = self.sentiment_df.groupby('date')['compound'].mean().reset_index()
            daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date'])
            daily_sentiment.set_index('date', inplace=True)
            self.stock_df.index = pd.to_datetime(self.stock_df.index)

            merged = self.stock_df[['Close']].join(daily_sentiment, how='inner')

            if merged.empty:
                messagebox.showwarning("No Data", "No matching dates found between stock and sentiment data.")
                return

            corr = merged['Close'].corr(merged['compound'])
            self.corr_label.config(text=f"📈 Correlation (Close vs Sentiment): {corr:.4f}")

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(merged.index, merged['Close'], label="Close Price", color="#00b4d8")
            ax.plot(merged.index, merged['compound'] * 100, label="Sentiment (scaled)", color="#ff006e", alpha=0.7)
            ax.set_title("Netflix Stock Close Price vs Sentiment (Compound)", fontsize=14)
            ax.legend()
            ax.grid(True)
            fig.tight_layout()

            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixSentimentApp(root)
    root.mainloop()
