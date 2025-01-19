import tkinter as tk
from tkinter import filedialog
import requests

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            response = requests.post('http://127.0.0.1:5000/upload', files={'file': file})
        if response.status_code == 200:
            status_label.config(text="Image uploaded successfully!")
        else:
            status_label.config(text="Failed to upload image.")

app = tk.Tk()
app.title("Image Uploader")

upload_button = tk.Button(app, text="Upload Image", command=upload_image)
upload_button.pack(pady=20)

status_label = tk.Label(app, text="")
status_label.pack(pady=20)

app.mainloop()
