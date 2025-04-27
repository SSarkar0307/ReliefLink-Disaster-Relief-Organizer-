from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import uvicorn
import markdown2
import threading
from disaster_simulator import router as disaster_router, generate_disasters
from routes.copy import router as auth_router
from fetch_aid_transfers import AidTransferFetcher

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
aid_fetcher = AidTransferFetcher()


# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(disaster_router)

# Mount static files to serve HTML and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Start the simulator thread on app startup
@app.on_event("startup")
def start_simulator():
    threading.Thread(target=generate_disasters, daemon=True).start()

# Pydantic model for chatbot request body
class ChatInput(BaseModel):
    text: str

# Groq API configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

@app.post("/chatbot")
async def chatbot(chat_input: ChatInput):
    user_input = chat_input.text

    if not user_input:
        return {"reply": "Please enter a message."}

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful disaster relief assistant. Always guide users with clear steps during floods, earthquakes, fires, and emergencies."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

        html_reply = markdown2.markdown(ai_reply)
        return {"reply": html_reply}
    except requests.exceptions.RequestException as e:
        return {"reply": f"API request failed: {str(e)}"}
    except KeyError as e:
        return {"reply": f"Unexpected response format: {str(e)}"}
    except Exception as e:
        return {"reply": f"An error occurred: {str(e)}"}

@app.get("/api/aid-transfers")
async def get_aid_transfers():
    return aid_fetcher.get_aid_transfers()

# Serve chatbot frontend
@app.get("/chatbot-page", response_class=HTMLResponse)
async def get_chatbot_page():
    with open("static/chatbot.html", "r") as f:
        return f.read()

# Serve disaster feed frontend
@app.get("/disaster-feed", response_class=HTMLResponse)
async def get_disaster_feed_page():
    with open("static/disaster-feed.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)