import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

class NetflixSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Stock & Sentiment Correlation")

        self.process_btn = tk.Button(root, text="Process and Plot", command=self.process_data)
        self.process_btn.pack(pady=10)

        self.corr_label = tk.Label(root, text="")
        self.corr_label.pack()

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
            df['date'] = df['datetime'].dt.date
            self.sentiment_df = df

            messagebox.showinfo("Success", "Data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")

    def process_data(self):
        try:
            daily_sentiment = self.sentiment_df.groupby('date')['compound'].mean().reset_index()
            daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date'])
            daily_sentiment.set_index('date', inplace=True)

            merged = self.stock_df[['Close']].join(daily_sentiment, how='inner')

            corr = merged['Close'].corr(merged['compound'])
            self.corr_label.config(text=f"Correlation (Close vs Compound Sentiment): {corr:.4f}")

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(merged.index, merged['Close'], label="Close Price")
            ax.plot(merged.index, merged['compound'] * 100, label="Sentiment (scaled)", alpha=0.7)
            ax.set_title("Netflix Stock Close Price vs Sentiment (Compound)")
            ax.legend()
            ax.grid(True)
            fig.tight_layout()

            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixSentimentApp(root)
    root.mainloop()
