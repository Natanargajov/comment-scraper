import os
import time
import csv
import tkinter as tk
from tkinter import messagebox
from apify_client import ApifyClient

def scrape_comments():
    post_url = entry_url.get().strip()
    if not post_url:
        messagebox.showerror("Error", "Masukkan URL post Instagram yang benar!")
        return

    try:
        APIFY_API_TOKEN = "apify_api_o7ut1S9GWqBg4g6x6TIvsmQXkHSmp80anJk6"
        client = ApifyClient(APIFY_API_TOKEN)
        messagebox.showinfo("Info", "Sedang melakukan scraping... Silahkan Tunggu.")
        run = client.actor("apify/instagram-comment-scraper").call(
            run_input={"directUrls": [post_url], "resultsLimit": 100}
        )

        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        # Generate filename unik
        timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        filename = f"instagram_comments_{timestamp}.csv"

        # Save to CSV
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Comment"])  # CSV Header

            for item in dataset_items:
                writer.writerow([item.get("username"), item.get("text")])

        messagebox.showinfo("Sukses", f"Komentar disimpan dengan format : {filename}")

    except Exception as e:
        messagebox.showerror("Error", f" Error: {str(e)}")

# Dark Mode GUI Window
root = tk.Tk()
root.title("Instagram Comment Scraper")
root.geometry("500x250")
root.configure(bg="#1e1e1e")  # Darkmode background
font_title = ("Helvetica", 14, "bold")
font_text = ("Helvetica", 12)

# Label & Input
tk.Label(root, text="Masukkan URL Post Instagram :", font=font_title, fg="white", bg="#1e1e1e").pack(pady=10)
entry_url = tk.Entry(root, width=50, font=font_text, bg="#333", fg="white", insertbackground="white", relief="flat")
entry_url.pack(pady=5)

# Scrape Button
btn_scrape = tk.Button(
    root, text="Scrape", font=font_text, bg="#008CBA", fg="white",
    activebackground="#005f7f", activeforeground="white", relief="flat",
    command=scrape_comments
)
btn_scrape.pack(pady=15)

# Run GUI
root.mainloop()
