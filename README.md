# 📄 Resume Analyzer

An AI-powered resume matching application that analyzes how well your resume matches job descriptions using machine learning.

## 🌟 Features

✅ **PDF Resume Upload** - Upload your resume and extract text automatically
✅ **Job Description Matching** - Paste job descriptions to compare
✅ **ML-Powered Analysis** - Uses TF-IDF and Cosine Similarity algorithms
✅ **Match Score Calculation** - Get a percentage match score (0-100%)
✅ **Skills Analysis** - Identifies matched and missing skills
✅ **Beautiful UI** - Modern, responsive design with Bootstrap 5
✅ **Local Processing** - All data processed locally, nothing sent to external servers
✅ **Analysis History** - Save and review past analyses

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.2 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | SQLite |
| **ML Engine** | Scikit-learn (TF-IDF, Cosine Similarity) |
| **PDF Processing** | PyMuPDF (fitz) |
| **Language** | Python 3.8+ |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/sushhh07/resume_analyzer.git
cd resume_analyzer
```

2. **Create a virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup the database**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional, for admin panel)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Open in browser**
```
http://localhost:8000
```

## 📖 How to Use

### Step 1: Home Page
- Visit the home page to understand the application
- Click "Start Analyzing" button

### Step 2: Upload Resume
- Click the upload area or drag & drop your PDF resume
- Maximum file size: 10MB
- Only PDF files are accepted

### Step 3: Enter Job Description
- Paste the complete job description in the text area
- Include job title, responsibilities, required skills, experience level
- Minimum 50 characters required

### Step 4: Analyze
- Click the "Analyze Resume" button
- Wait for processing (typically 2-5 seconds)

### Step 5: Review Results
- View your match score (0-100%)
- See matched skills (in green)
- See missing skills (in red)
- Get recommendations based on your match score

## 🧠 Machine Learning Pipeline

### 1. **Text Extraction**
   - Extract text from PDF using PyMuPDF
   - Handle multi-page documents

### 2. **Text Preprocessing**
   - Convert to lowercase
   - Remove URLs and email addresses
   - Remove special characters
   - Remove stop words
   - Clean extra whitespace

### 3. **TF-IDF Vectorization** (Machine Learning)
   - Convert text to numerical vectors
   - Max features: 500
   - Includes unigrams and bigrams
   - Scikit-learn's TfidfVectorizer

### 4. **Cosine Similarity** (Machine Learning)
   - Compare resume and job description vectors
   - Calculate angle between vectors
   - Convert to percentage (0-100%)

### 5. **Skills Matching**
   - Extract important keywords from both documents
   - Identify intersection (matched skills)
   - Identify difference (missing skills)

## 📁 Project Structure

```
resume_analyzer/
├── manage.py                          # Django management script
├── requirements.txt                   # Project dependencies
├── db.sqlite3                         # SQLite database
│
├── resume_analyzer_project/           # Django project settings
│   ├── __init__.py
│   ├── settings.py                    # Django configuration
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI application
│
├── analyzer/                          # Django app
│   ├── migrations/                    # Database migrations
│   ├── templates/
│   │   └── analyzer/                  # App templates
│   │       ├── index.html             # Home page
│   │       ├── analyze.html           # Upload form
│   │       └── results.html           # Results page
│   │
│   ├── __init__.py
│   ├── admin.py                       # Django admin config
│   ├── apps.py                        # App configuration
│   ├── forms.py                       # Django forms
│   ├── models.py                      # Database models
│   ├── views.py                       # View functions
│   ├── urls.py                        # App URL routes
│   └── ml_utils.py                    # Machine learning logic
│
├── templates/
│   └── base.html                      # Base template
│
├── static/                            # Static files (CSS, JS, images)
│
└── media/                             # User uploads (resumes, etc)
```

## 🔧 Configuration

### Settings (resume_analyzer_project/settings.py)

```python
# Maximum file upload size (10MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# TF-IDF Configuration
MAX_FEATURES = 500          # Maximum vocabulary size
MIN_DF = 1                  # Minimum document frequency
MAX_DF = 0.95              # Maximum document frequency
```

## 📊 Match Score Interpretation

| Score Range | Interpretation | Recommendation |
|-------------|----------------|----------------|
| 80-100% | Excellent fit | Apply immediately |
| 60-79% | Good match | You have most skills |
| 40-59% | Fair match | Consider learning missing skills |
| 0-39% | Poor match | May not be a good fit |

## 🗄️ Database Models

### ResumeAnalysis Model

```python
fields:
    - id: Auto-generated primary key
    - resume_file: Uploaded PDF file
    - resume_text: Extracted text from resume
    - job_description: Job description entered by user
    - match_score: Calculated match percentage (0-100)
    - matched_skills: Comma-separated matched skills
    - missing_skills: Comma-separated missing skills
    - created_at: Timestamp of analysis
    - updated_at: Last update timestamp
```

## 🔐 Privacy & Security

✅ **No Cloud Storage** - All files processed locally
✅ **No External APIs** - Independent processing
✅ **No Data Transmission** - Nothing sent to external servers
✅ **Local Database** - SQLite database on your machine
✅ **Secure File Upload** - PDF validation and file size limits

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fitz'"
**Solution:** Install PyMuPDF
```bash
pip install pymupdf
```

### Issue: "Port 8000 already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

### Issue: "Database migration errors"
**Solution:** Reset migrations
```bash
python manage.py migrate analyzer zero
python manage.py migrate
```

### Issue: "PDF upload fails"
**Solution:** Ensure file is valid PDF and under 10MB

## 📝 Sample Job Description

```
Senior Python Developer

We are looking for a Senior Python Developer with 5+ years of experience.

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Django framework
- Experience with REST APIs
- PostgreSQL and database design
- Familiar with Git and version control
- Experience with Docker and containerization
- Knowledge of AWS or cloud platforms
- Unit testing and CI/CD pipelines

Responsibilities:
- Develop and maintain backend services
- Write clean, maintainable code
- Collaborate with team members
- Participate in code reviews
- Optimize application performance
```

## 🚀 Deployment

### To production servers (e.g., Heroku, AWS, DigitalOcean):

1. Change `DEBUG = False` in settings.py
2. Add domain to `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set `SECRET_KEY` from environment variable
5. Configure static files serving
6. Enable HTTPS

## 📈 Future Enhancements

- [ ] Advanced ML models (Word2Vec, BERT)
- [ ] Resume formatting extraction
- [ ] Batch analysis for multiple resumes
- [ ] Export results to PDF
- [ ] Email notifications
- [ ] User authentication and profiles
- [ ] Analysis history and comparisons
- [ ] API for third-party integration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Sushant Srivastava**
- GitHub: [@sushhh07](https://github.com/sushhh07)
- Email: suhanisrivastav6@gmail.com

## ❓ FAQ

**Q: Can I analyze multiple resumes?**
A: Yes, just click "Analyze Another Resume" after viewing results.

**Q: How accurate is the matching?**
A: The ML model uses industry-standard TF-IDF and cosine similarity. Accuracy depends on how well job descriptions are written.

**Q: Is my data safe?**
A: Yes, all processing is local. No data is sent to external servers.

**Q: Can I see my previous analyses?**
A: Not in the current version, but you can check the admin panel if you have access.

**Q: What file formats are supported?**
A: Currently only PDF files are supported.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: suhanisrivastav6@gmail.com

---

⭐ If you find this project useful, please give it a star on GitHub!
