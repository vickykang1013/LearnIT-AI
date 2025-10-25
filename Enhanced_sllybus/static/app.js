// Global variables
let currentSchedule = null;
let completedTasks = new Set();

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set default start date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('startDate').value = today;
    
    // Setup file upload handlers
    setupFileUpload();
    
    // Setup generate button
    document.getElementById('generateBtn').addEventListener('click', generateSchedule);
}

function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('active');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('active');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('active');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    const validTypes = ['application/pdf', 'text/plain', 'text/markdown'];
    
    if (!validTypes.includes(file.type) && !file.name.endsWith('.md')) {
        alert('Please upload a PDF, TXT, or MD file');
        return;
    }
    
    // Update UI to show file name
    const uploadText = document.querySelector('.upload-text .primary-text');
    uploadText.textContent = `📄 ${file.name} uploaded`;
    
    if (file.type === 'application/pdf') {
        // Handle PDF extraction
        const reader = new FileReader();
        reader.onload = async function(e) {
            try {
                const response = await fetch('/extract-pdf', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ file_data: e.target.result })
                });
                
                const data = await response.json();
                if (data.text) {
                    document.getElementById('syllabusText').value = data.text;
                } else if (data.error) {
                    alert('Error extracting PDF: ' + data.error);
                }
            } catch (error) {
                alert('Failed to extract PDF content');
                console.error(error);
            }
        };
        reader.readAsDataURL(file);
    } else {
        // Handle text files
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('syllabusText').value = e.target.result;
        };
        reader.readAsText(file);
    }
}

async function generateSchedule() {
    const syllabusText = document.getElementById('syllabusText').value.trim();
    const duration = parseInt(document.getElementById('duration').value);
    const startDate = document.getElementById('startDate').value;
    
    if (!syllabusText) {
        alert('Please provide syllabus content');
        return;
    }
    
    // Show loading state
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    try {
        const response = await fetch('/generate-schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                syllabus: syllabusText,
                duration: duration,
                start_date: startDate
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        currentSchedule = data;
        displaySchedule(data);
        
    } catch (error) {
        alert('Error generating schedule: ' + error.message);
        console.error(error);
    } finally {
        document.getElementById('generateBtn').disabled = false;
        document.getElementById('loadingState').style.display = 'none';
    }
}

function displaySchedule(schedule) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('progressTracker').style.display = 'block';
    
    // Calculate and display stats
    displayStats(schedule);
    
    // Build schedule HTML
    const container = document.getElementById('scheduleContainer');
    container.innerHTML = '';
    
    if (schedule.summary) {
        const summaryDiv = document.createElement('div');
        summaryDiv.className = 'schedule-summary';
        summaryDiv.innerHTML = `
            <h3>📋 Course Overview</h3>
            <p>${schedule.summary}</p>
        `;
        container.appendChild(summaryDiv);
    }
    
    // Add each week
    schedule.weeks.forEach(week => {
        const weekCard = createWeekCard(week);
        container.appendChild(weekCard);
    });
    
    // Smooth scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function displayStats(schedule) {
    let totalHours = 0;
    let totalVideos = 0;
    let totalQuizzes = 0;
    
    schedule.weeks.forEach(week => {
        week.days.forEach(day => {
            totalHours += day.estimated_hours || 2;
            totalVideos += (day.youtube_searches || []).length;
            totalQuizzes += (day.quiz_questions || []).length;
        });
    });
    
    document.getElementById('totalWeeks').textContent = schedule.weeks.length;
    document.getElementById('totalHours').textContent = Math.round(totalHours);
    document.getElementById('totalVideos').textContent = totalVideos;
    document.getElementById('totalQuizzes').textContent = totalQuizzes;
}

function createWeekCard(week) {
    const weekDiv = document.createElement('div');
    weekDiv.className = 'week-card';
    weekDiv.innerHTML = `
        <div class="week-header">
            <h3 class="week-title">Week ${week.week_number}: ${week.title || 'Study Week'}</h3>
            <span class="week-toggle">▼</span>
        </div>
        ${week.overview ? `<p class="week-overview">${week.overview}</p>` : ''}
        <div class="week-days">
            ${week.days.map(day => createDayItem(day, week.week_number)).join('')}
        </div>
    `;
    
    // Add toggle functionality
    const header = weekDiv.querySelector('.week-header');
    const daysContainer = weekDiv.querySelector('.week-days');
    header.addEventListener('click', () => {
        daysContainer.style.display = daysContainer.style.display === 'none' ? 'block' : 'none';
        weekDiv.querySelector('.week-toggle').textContent = 
            daysContainer.style.display === 'none' ? '▶' : '▼';
    });
    
    return weekDiv;
}

function createDayItem(day, weekNumber) {
    const dayId = `day-${weekNumber}-${day.day}`;
    const isCompleted = completedTasks.has(dayId);
    
    return `
        <div class="day-item ${isCompleted ? 'completed' : ''}" id="${dayId}">
            <div class="day-header">
                <div>
                    <span class="day-date">${day.day}</span>
                    ${day.date ? `<small> (${formatDate(day.date)})</small>` : ''}
                </div>
                <span class="day-hours">⏱️ ${day.estimated_hours || 2} hours</span>
            </div>
            
            <h4 class="day-topic">${day.topic}</h4>
            
            ${day.objectives && day.objectives.length > 0 ? `
                <ul class="day-objectives">
                    ${day.objectives.map(obj => `<li>${obj}</li>`).join('')}
                </ul>
            ` : ''}
            
            <div class="resource-links">
                ${day.youtube_links && day.youtube_links.map(link => `
                    <a href="${link.url}" target="_blank" class="resource-link youtube-link">
                        <i class="fab fa-youtube"></i> ${link.term}
                    </a>
                `).join('')}
                
                ${day.quiz_questions && day.quiz_questions.length > 0 ? `
                    <button class="resource-link quiz-link" onclick="showQuiz('${dayId}', ${JSON.stringify(day.quiz_questions).replace(/"/g, '&quot;')})">
                        <i class="fas fa-question-circle"></i> Take Quiz (${day.quiz_questions.length} questions)
                    </button>
                ` : ''}
                
                <button class="resource-link" onclick="markComplete('${dayId}')">
                    <i class="fas ${isCompleted ? 'fa-check-square' : 'fa-square'}"></i>
                    ${isCompleted ? 'Completed' : 'Mark Complete'}
                </button>
            </div>
        </div>
    `;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function showQuiz(dayId, questions) {
    const modal = document.getElementById('quizModal');
    const content = document.getElementById('quizContent');
    
    content.innerHTML = questions.map((q, index) => `
        <div class="quiz-question" data-correct="${q.correct}">
            <h4>Question ${index + 1}: ${q.question}</h4>
            <ul class="quiz-options">
                ${q.options.map((opt, i) => `
                    <li data-index="${i}" onclick="checkAnswer(this, ${i}, ${q.correct})">
                        ${opt}
                    </li>
                `).join('')}
            </ul>
            <div class="quiz-explanation" style="display: none;">
                💡 ${q.explanation || 'Great job!'}
            </div>
        </div>
    `).join('');
    
    modal.style.display = 'flex';
}

function checkAnswer(element, selected, correct) {
    const question = element.closest('.quiz-question');
    const options = question.querySelectorAll('.quiz-options li');
    
    // Disable all options
    options.forEach(opt => {
        opt.style.pointerEvents = 'none';
    });
    
    // Mark correct and incorrect
    if (selected === correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
        options[correct].classList.add('correct');
    }
    
    // Show explanation
    question.querySelector('.quiz-explanation').style.display = 'block';
}

function closeQuiz() {
    document.getElementById('quizModal').style.display = 'none';
}

function markComplete(dayId) {
    const dayElement = document.getElementById(dayId);
    const button = dayElement.querySelector('.resource-link:last-child');
    
    if (completedTasks.has(dayId)) {
        completedTasks.delete(dayId);
        dayElement.classList.remove('completed');
        button.innerHTML = '<i class="fas fa-square"></i> Mark Complete';
    } else {
        completedTasks.add(dayId);
        dayElement.classList.add('completed');
        button.innerHTML = '<i class="fas fa-check-square"></i> Completed';
    }
    
    updateProgress();
    saveProgress();
}

function updateProgress() {
    if (!currentSchedule) return;
    
    const totalDays = currentSchedule.weeks.reduce((acc, week) => acc + week.days.length, 0);
    const completedDays = completedTasks.size;
    const percentage = Math.round((completedDays / totalDays) * 100);
    
    document.getElementById('progressFill').style.width = percentage + '%';
    document.getElementById('progressPercent').textContent = percentage;
}

function saveProgress() {
    // Save to localStorage for persistence
    localStorage.setItem('studyProgress', JSON.stringify(Array.from(completedTasks)));
    
    // Optional: Save to backend
    fetch('/save-progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            completed: Array.from(completedTasks),
            schedule_id: currentSchedule?.id || 'default'
        })
    });
}

function loadProgress() {
    const saved = localStorage.getItem('studyProgress');
    if (saved) {
        completedTasks = new Set(JSON.parse(saved));
        updateProgress();
    }
}

async function exportCalendar() {
    if (!currentSchedule) {
        alert('Please generate a schedule first');
        return;
    }
    
    try {
        const response = await fetch('/export-calendar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ schedule: currentSchedule })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `study_schedule_${new Date().toISOString().split('T')[0]}.ics`;
            a.click();
        }
    } catch (error) {
        alert('Failed to export calendar');
        console.error(error);
    }
}

function printSchedule() {
    window.print();
}

function shareSchedule() {
    if (!currentSchedule) {
        alert('Please generate a schedule first');
        return;
    }
    
    const shareData = {
        title: 'My Study Schedule',
        text: `Check out my ${currentSchedule.weeks.length}-week study plan!`,
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData);
    } else {
        // Fallback: Copy to clipboard
        const scheduleText = formatScheduleAsText(currentSchedule);
        navigator.clipboard.writeText(scheduleText).then(() => {
            alert('Schedule copied to clipboard!');
        });
    }
}

function formatScheduleAsText(schedule) {
    let text = '📚 STUDY SCHEDULE\n\n';
    
    schedule.weeks.forEach(week => {
        text += `WEEK ${week.week_number}: ${week.title || 'Study Week'}\n`;
        text += week.overview ? `${week.overview}\n\n` : '\n';
        
        week.days.forEach(day => {
            text += `  ${day.day}: ${day.topic}\n`;
            if (day.objectives) {
                day.objectives.forEach(obj => {
                    text += `    • ${obj}\n`;
                });
            }
            text += '\n';
        });
    });
    
    return text;
}

// Load saved progress on startup
loadProgress();

// Add completed styling
const style = document.createElement('style');
style.textContent = `
    .day-item.completed {
        opacity: 0.7;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
        border-left: 3px solid var(--success-color);
    }
`;
document.head.appendChild(style);