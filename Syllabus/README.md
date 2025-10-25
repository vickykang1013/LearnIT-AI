# 📅 Syllabus Study Planner

An AI-powered tool that transforms your course syllabus into a detailed, week-by-week study schedule with YouTube resource recommendations.

## 🌟 Features

- **Smart Schedule Generation**: Creates personalized study plans based on your syllabus
- **Flexible Duration**: Support for courses from 1-52 weeks
- **Daily Breakdown**: 5 study days per week with specific objectives
- **YouTube Resources**: Suggests relevant search terms for each topic
- **Clean Interface**: Easy-to-use web interface with file upload support
- **Copy & Export**: Copy your schedule or print it for offline use

## 🚀 Quick Start

### 1. Get Your Groq API Key (FREE)
1. Visit [console.groq.com](https://console.groq.com/keys)
2. Sign up and create a new API key
3. Copy your key

### 2. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your API key to .env
# GROQ_API_KEY=your_actual_key_here
```

### 3. Run the App

```bash
python syllabus_planner.py
```

Visit `http://localhost:5002` in your browser

## 📖 How to Use

1. **Enter Course Duration**: Specify how many weeks your course runs (default: 10 weeks)

2. **Add Your Syllabus**: Either:
   - Paste your syllabus text directly into the text area
   - Upload a .txt or .md file containing your syllabus

3. **Generate Schedule**: Click "Generate Study Schedule" and wait ~10-30 seconds

4. **Review & Use**: 
   - Review your personalized week-by-week schedule
   - Click "Copy" to copy the entire schedule
   - Use the YouTube search terms to find learning resources

## 📝 Example Syllabus Input

```
Course: Introduction to Python Programming

Topics Covered:
- Python basics and syntax
- Data types and variables
- Control flow (if/else, loops)
- Functions and modules
- Object-oriented programming
- File handling
- Error handling and debugging
- Working with libraries (pandas, numpy)
- Final project

Learning Objectives:
- Understand fundamental programming concepts
- Write clean, efficient Python code
- Build real-world applications
```

## 🎯 What You Get

For each week, you'll receive:
- **Week overview** with main topics
- **Daily objectives** (Monday-Friday)
- **Specific learning goals** for each day
- **YouTube search terms** for finding video tutorials
- **Realistic workload** (2-3 hours per day)

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Groq API (llama-3.3-70b-versatile)
- **Frontend**: Vanilla HTML/CSS/JavaScript

## 📋 Requirements

- Python 3.7+
- Free Groq API key
- Modern web browser

## 🔧 Configuration

The app runs on port 5002 by default. To change:

```python
# In syllabus_planner.py, modify:
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

## 💡 Tips

- **Be detailed**: More detailed syllabi produce better schedules
- **Include objectives**: Mention learning goals and outcomes
- **List resources**: Include any textbooks or materials mentioned
- **Realistic duration**: Match the actual course length for best results

## 🤝 Future Enhancements

- PDF syllabus upload support
- Export to PDF/Google Calendar
- Progress tracking
- Integration with more learning platforms
- Custom study intensity levels

## 📄 License

Free to use and modify for personal and educational purposes.

---

**Built with ❤️ using Groq AI**
