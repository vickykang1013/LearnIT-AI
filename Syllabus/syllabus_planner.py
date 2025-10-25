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

logger.info("🚀 Starting Syllabus Study Planner with Groq API")
logger.info(f"API Key present: {'Yes' if GROQ_API_KEY else 'No'}")

@app.route("/")
def home():
    return render_template("planner.html")

@app.route("/generate-schedule", methods=["POST"])
def generate_schedule():
    if not GROQ_API_KEY:
        return jsonify({"error": "⚠️ Please set GROQ_API_KEY in .env file"})
    
    syllabus_text = request.json.get("syllabus", "").strip()
    duration_weeks = request.json.get("duration", 10)
    
    if not syllabus_text:
        return jsonify({"error": "Please provide syllabus content!"})
    
    logger.info(f"📚 Generating schedule for {duration_weeks} weeks")
    logger.info(f"Syllabus length: {len(syllabus_text)} characters")
    
    # Create detailed prompt for Groq
    system_msg = """You are an expert academic planner. Create a detailed week-by-week, day-by-day study schedule based on the provided syllabus.

For each week, provide:
1. Week number and main topics
2. Daily breakdown (5 study days per week)
3. Specific learning objectives for each day
4. Suggested YouTube search terms (be specific but general enough to find content)

Format your response as clean, structured text with clear headings."""

    user_prompt = f"""Based on this syllabus, create a {duration_weeks}-week study schedule:

SYLLABUS:
{syllabus_text}

REQUIREMENTS:
- Break down into {duration_weeks} weeks
- 5 study days per week (Monday-Friday)
- Each day should have specific topics and objectives
- Suggest relevant YouTube search terms for key concepts
- Be realistic about daily workload (2-3 hours per day)
- Include review days before major topics

Format each week clearly with:
**WEEK X: [Main Topic]**
- Monday: [Topic] - [Objectives] | YouTube: "[search term]"
- Tuesday: [Topic] - [Objectives] | YouTube: "[search term]"
etc."""

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
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 3000
            },
            timeout=60
        )
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({"error": f"⚠️ API Error: {response.status_code}"})
        
        data = response.json()
        schedule = data["choices"][0]["message"]["content"]
        
        logger.info(f"✅ Generated schedule: {len(schedule)} characters")
        return jsonify({"schedule": schedule})
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({"error": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("\n⚠️  Get a FREE Groq API key at: https://console.groq.com/keys")
        print("Add to .env: GROQ_API_KEY=your_key_here\n")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
