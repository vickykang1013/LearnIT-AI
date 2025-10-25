from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from dotenv import load_dotenv
import logging
import PyPDF2
import io
import base64
from datetime import datetime, timedelta
import json
import re
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

logger.info("🚀 Starting Enhanced Syllabus Study Planner")
logger.info(f"API Key present: {'Yes' if GROQ_API_KEY else 'No'}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/extract-pdf", methods=["POST"])
def extract_pdf():
    """Extract text from uploaded PDF"""
    try:
        file_data = request.json.get("file_data", "")
        if not file_data:
            return jsonify({"error": "No file data provided"})
        
        # Decode base64 PDF data
        pdf_data = base64.b64decode(file_data.split(",")[1])
        pdf_file = io.BytesIO(pdf_data)
        
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        logger.info(f"📄 Extracted {len(text)} characters from PDF")
        return jsonify({"text": text})
        
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return jsonify({"error": f"Failed to extract PDF: {str(e)}"})

@app.route("/generate-schedule", methods=["POST"])
def generate_schedule():
    if not GROQ_API_KEY:
        return jsonify({"error": "⚠️ Please set GROQ_API_KEY in .env file"})
    
    syllabus_text = request.json.get("syllabus", "").strip()
    duration_weeks = request.json.get("duration", 10)
    start_date = request.json.get("start_date", datetime.now().strftime("%Y-%m-%d"))
    
    if not syllabus_text:
        return jsonify({"error": "Please provide syllabus content!"})
    
    logger.info(f"📚 Generating schedule for {duration_weeks} weeks starting {start_date}")
    
    system_msg = """You are an expert academic planner and educational content curator. Create a comprehensive study schedule with YouTube videos and quiz questions.

For each week, provide a JSON response with the following structure:
{
  "weeks": [
    {
      "week_number": 1,
      "title": "Week Title",
      "overview": "Brief overview",
      "days": [
        {
          "day": "Monday",
          "date": "YYYY-MM-DD",
          "topic": "Main topic",
          "objectives": ["Objective 1", "Objective 2"],
          "subtopics": ["Subtopic 1", "Subtopic 2"],
          "youtube_searches": ["specific search term 1", "specific search term 2"],
          "estimated_hours": 2.5,
          "quiz_questions": [
            {
              "question": "Question text?",
              "options": ["A", "B", "C", "D"],
              "correct": 0,
              "explanation": "Why this answer is correct"
            }
          ]
        }
      ]
    }
  ],
  "summary": "Overall course summary"
}

Create realistic, achievable daily goals with 2-3 hours of study time. Include review sessions and practice days."""

    user_prompt = f"""Create a {duration_weeks}-week study schedule starting from {start_date} based on this syllabus:

SYLLABUS:
{syllabus_text[:3000]}  # Limit to avoid token issues

Requirements:
- {duration_weeks} weeks total
- 5 study days per week (Monday-Friday)
- 2-3 hours per day
- Include 2-3 quiz questions per major topic
- Provide specific YouTube search terms that will find good educational content
- Add review days before exams/major topics
- Progressive difficulty
- Include practical exercises where applicable

Return a properly formatted JSON response."""

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
                "max_tokens": 4000,
                "response_format": {"type": "json_object"}
            },
            timeout=60
        )
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return jsonify({"error": f"API Error: {response.status_code}"})
        
        data = response.json()
        schedule_json = json.loads(data["choices"][0]["message"]["content"])
        
        # Add YouTube video links
        schedule_json = add_youtube_links(schedule_json)
        
        logger.info(f"✅ Generated comprehensive schedule")
        return jsonify(schedule_json)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return jsonify({"error": "Failed to parse schedule data"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": f"Error: {str(e)}"})

def add_youtube_links(schedule):
    """Add actual YouTube search links to the schedule"""
    youtube_base = "https://www.youtube.com/results?search_query="
    
    for week in schedule.get("weeks", []):
        for day in week.get("days", []):
            youtube_links = []
            for search_term in day.get("youtube_searches", []):
                # Create YouTube search URL
                encoded_term = quote(search_term + " tutorial education")
                youtube_links.append({
                    "term": search_term,
                    "url": youtube_base + encoded_term
                })
            day["youtube_links"] = youtube_links
    
    return schedule

@app.route("/export-calendar", methods=["POST"])
def export_calendar():
    """Export schedule as iCalendar file"""
    try:
        schedule = request.json.get("schedule", {})
        
        # Create iCalendar content
        ical_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Study Planner//hackathon//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""
        
        for week in schedule.get("weeks", []):
            for day in week.get("days", []):
                date = day.get("date", "")
                if date:
                    dt = datetime.strptime(date, "%Y-%m-%d")
                    ical_content += f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{dt.strftime("%Y%m%d")}
DTEND;VALUE=DATE:{(dt + timedelta(days=1)).strftime("%Y%m%d")}
SUMMARY:📚 {day.get('topic', 'Study Session')}
DESCRIPTION:Objectives: {', '.join(day.get('objectives', []))}\\nEstimated: {day.get('estimated_hours', 2)} hours
END:VEVENT
"""
        
        ical_content += "END:VCALENDAR"
        
        # Save to file
        filename = f"study_schedule_{datetime.now().strftime('%Y%m%d')}.ics"
        filepath = f"/tmp/{filename}"
        with open(filepath, "w") as f:
            f.write(ical_content)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({"error": f"Export failed: {str(e)}"})

@app.route("/save-progress", methods=["POST"])
def save_progress():
    """Save user's study progress"""
    try:
        progress_data = request.json
        # In production, save to database
        # For hackathon, just return success
        return jsonify({"success": True, "message": "Progress saved!"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("\n⚠️  Get a FREE Groq API key at: https://console.groq.com/keys")
        print("Add to .env: GROQ_API_KEY=your_key_here\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
