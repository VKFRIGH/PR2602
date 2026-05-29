import webbrowser
import threading
import os
import time

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8501")

threading.Thread(target=open_browser).start()

os.system("python -m streamlit run app.py")