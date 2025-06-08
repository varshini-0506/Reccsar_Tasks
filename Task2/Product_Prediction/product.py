import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import tkinter as tk
from tkinter import messagebox

class ProductRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Product Recommendation Visualizer")
        self.root.geometry("1000x600")
        self.root.config(bg="#1f1f2e")

        title = tk.Label(root, text="📦 Product Recommendation Visualizer", font=("Helvetica", 16, "bold"), bg="#1f1f2e", fg="white")
        title.pack(pady=10)

        process_btn = tk.Button(root, text="Load & Visualize", command=self.process_data, font=("Arial", 12), bg="#5a9", fg="white")
        process_btn.pack(pady=10)

        self.plot_frame = tk.Frame(root, bg="#1f1f2e")
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def process_data(self):
        try:
            # Load data
            df = pd.read_csv("product_data.csv", usecols=['event_time', 'event_type', 'product_id', 'user_id'])
            df = df[df['event_type'] == 'view']

            # Keep only top 500 products and users to reduce load
            top_users = df['user_id'].value_counts().nlargest(500).index
            top_products = df['product_id'].value_counts().nlargest(50).index
            df = df[df['user_id'].isin(top_users) & df['product_id'].isin(top_products)]

            # Create interaction matrix
            matrix = df.pivot_table(index='user_id', columns='product_id', aggfunc=len, fill_value=0)

            # Transpose for product-based cosine similarity
            product_vectors = matrix.T
            sim_matrix = cosine_similarity(product_vectors)

            sim_df = pd.DataFrame(sim_matrix, index=product_vectors.index, columns=product_vectors.index)

            # Plot similarity heatmap and PCA scatter
            fig, axs = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle("Product Similarity Visualizations")

            # Heatmap
            im = axs[0].imshow(sim_df, cmap="coolwarm")
            axs[0].set_xticks(np.arange(len(sim_df.columns)))
            axs[0].set_yticks(np.arange(len(sim_df.index)))
            axs[0].set_xticklabels(sim_df.columns, rotation=90, fontsize=6)
            axs[0].set_yticklabels(sim_df.index, fontsize=6)
            axs[0].set_title("Cosine Similarity Heatmap")
            fig.colorbar(im, ax=axs[0])

            # PCA Plot
            pca = PCA(n_components=2)
            reduced = pca.fit_transform(sim_matrix)
            axs[1].scatter(reduced[:, 0], reduced[:, 1], alpha=0.7)
            for i, product in enumerate(sim_df.columns):
                axs[1].annotate(str(product), (reduced[i, 0], reduced[i, 1]), fontsize=6)
            axs[1].set_title("PCA Clustering of Products")

            # Embed in Tkinter
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))


# Launch app
root = tk.Tk()
app = ProductRecommenderApp(root)
root.mainloop()
