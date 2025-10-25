from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

logger.info("🚀 Starting StudyBuddy with Groq API")
logger.info(f"API Key present: {'Yes' if GROQ_API_KEY else 'No'}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"reply": "⚠️ Please set GROQ_API_KEY in .env file"})
    
    user_input = request.json.get("message", "").strip()
    difficulty = request.json.get("difficulty", "high school")
    
    if not user_input:
        return jsonify({"reply": "Please enter a question!"})
    
    logger.info(f"📥 Question: {user_input}")
    
    # Create system message based on difficulty
    if difficulty == "child":
        system_msg = "You are a friendly tutor explaining things simply for young children (age 5-8). Use simple words and fun examples."
    elif difficulty == "high school":
        system_msg = "You are a helpful tutor explaining concepts at a high school level. Be clear and educational."
    else:
        system_msg = "You are an expert tutor providing detailed college-level explanations with technical depth."
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({"reply": f"⚠️ API Error: {response.status_code}"})
        
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        
        logger.info(f"✅ Generated answer: {answer[:100]}...")
        return jsonify({"reply": answer})
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({"reply": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("\n⚠️  Get a FREE Groq API key at: https://console.groq.com/keys")
        print("Add to .env: GROQ_API_KEY=your_key_here\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)