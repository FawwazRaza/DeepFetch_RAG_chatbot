import os
import threading
import time
from pyngrok import ngrok

os.system("uvicorn test_backend:app --host 0.0.0.0 --port 8000 &")

time.sleep(3)

public_url = ngrok.connect(8000).public_url
print(f"FastAPI backend is live at: {public_url}")

with open("backend_url.txt", "w") as f:
    f.write(public_url)
