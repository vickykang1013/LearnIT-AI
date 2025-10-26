# 📚 LearnIt AI - Smart Syllabus Scheduler

Transform your course syllabus into a personalized, AI-powered study schedule complete with YouTube video resources and interactive quizzes!

## ✨ Features

- **📄 PDF Upload Support** - Upload syllabus PDFs directly or paste text
- **🎯 AI-Powered Scheduling** - Intelligent weekly and daily study plans
- **📺 YouTube Integration** - Curated video links for each topic
- **🧠 Quiz Generation** - Auto-generated quizzes to test your knowledge
- **📊 Progress Tracking** - Visual progress indicators and completion tracking
- **📅 Calendar Export** - Export your schedule to calendar apps
- **📱 Responsive Design** - Works on desktop, tablet, and mobile
- **🎨 Modern UI** - Clean, intuitive interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (FREE - get it at [console.groq.com](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo>
cd learnit-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 📖 How to Use

1. **Upload Your Syllabus**
   - Drag and drop a PDF file OR
   - Click to browse and select a file OR
   <!-- - Paste syllabus text directly -->

2. **Configure Settings**
   - Select course duration (4-16 weeks)
   - Choose start date

3. **Generate Schedule**
   - Click "Generate Study Plan"
   - Wait for AI to process (10-20 seconds)

4. **Use Your Schedule**
   - View week-by-week breakdown
   - Click YouTube links for video tutorials
   - Take quizzes to test understanding
   - Mark days as complete
   - Export to calendar

## 🎯 Key Features Explained

### Smart Schedule Generation
- AI analyzes your syllabus content
- Creates realistic 2-3 hour daily study sessions
- Includes review days before major topics
- Progressive difficulty curve

### YouTube Resource Integration
- Specific search terms for each topic
- Direct links to YouTube searches
- Curated for educational content

### Interactive Quizzes
- Multiple choice questions for each major topic
- Instant feedback with explanations
- Track your understanding

### Progress Tracking
- Visual progress bar
- Persistent progress (saves locally)
- Completion statistics

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Groq API (Llama 3.3 70B)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **PDF Processing**: PyPDF2
- **Icons**: Font Awesome
- **Styling**: Custom CSS with modern design

## 📝 API Configuration

The app uses Groq's free API tier which provides:
- Fast inference speeds
- High-quality Llama 3.3 70B model
- Generous free tier limits
- No credit card required

## 🎨 Customization

You can customize the app by modifying:
- `static/styles.css` - Visual styling
- `static/app.js` - Frontend behavior
- `templates/index.html` - UI structure
- `app.py` - Backend logic and prompts

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use for your hackathon!

## 🏆 Hackathon Features

Perfect for hackathons because:
- ✅ Solves real student problem
- ✅ Uses cutting-edge AI
- ✅ Clean, modern UI
- ✅ Practical and useful
- ✅ Easy to demo
- ✅ Scalable concept

## 💡 Future Enhancements

Potential additions for hackathon judging:
- Integration with learning platforms (Coursera, edX)
- Collaborative study groups
- AI tutoring chatbot
- Spaced repetition algorithms
- Mobile app version
- Study streak gamification
- Note-taking integration
- Flashcard generation

## 🐛 Troubleshooting

**PDF extraction issues?**
- Ensure PDF contains selectable text (not scanned images)
- Try copy-pasting text manually

**API errors?**
- Verify Groq API key is correct
- Check internet connection
- Ensure API quota not exceeded

**Schedule not generating?**
- Provide detailed syllabus content
- Check browser console for errors
- Try shorter duration first

## 📧 Contact

Created for [Hackathon Name] by [Your Team]

---

**Good luck with your hackathon! 🚀**