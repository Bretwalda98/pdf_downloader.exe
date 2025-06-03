import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading

def download_pdfs(url, save_dir):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        pdf_links = [link['href'] for link in links if link['href'].lower().endswith('.pdf')]

        if not pdf_links:
            messagebox.showinfo("No PDFs Found", "No PDF links found on the provided page.")
            return

        for link in pdf_links:
            filename = os.path.basename(link.split('?')[0])
            filepath = os.path.join(save_dir, filename)
            full_url = link if link.startswith('http') else requests.compat.urljoin(url, link)
            with requests.get(full_url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        messagebox.showinfo("Download Complete", f"Downloaded {len(pdf_links)} PDFs to:\n{save_dir}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_path.set(folder)

def start_download():
    url = url_entry.get()
    save_dir = save_path.get()
    if not url or not save_dir:
        messagebox.showwarning("Input Missing", "Please enter a URL and select a folder.")
        return
    threading.Thread(target=download_pdfs, args=(url, save_dir), daemon=True).start()

root = tk.Tk()
root.title("PDF Downloader")

tk.Label(root, text="Webpage URL:").grid(row=0, column=0, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Save Folder:").grid(row=1, column=0, sticky="e")
save_path = tk.StringVar()
tk.Entry(root, textvariable=save_path, width=38).grid(row=1, column=1, padx=5, pady=5, sticky="w")
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=5)

tk.Button(root, text="Download PDFs", command=start_download, bg="green", fg="white").grid(row=2, column=1, pady=10)

root.mainloop()
