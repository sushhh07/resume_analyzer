# Setup Instructions for Resume Analyzer

## 🖥️ System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB free space
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## 📋 Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database migrations completed
- [ ] Server running
- [ ] Browser test passed

## 🔧 Detailed Setup Steps

### Step 1: Install Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click Install

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip python3-venv
```

Verify installation:
```bash
python --version
pip --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/sushhh07/resume_analyzer.git
cd resume_analyzer
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.7
- PyMuPDF 1.23.5 (PDF processing)
- scikit-learn 1.3.2 (Machine Learning)
- numpy 1.24.3 (Numerical computing)
- python-dotenv 1.0.0 (Environment variables)
- Pillow 10.0.1 (Image processing)

### Step 5: Setup Database

**Create migrations:**
```bash
python manage.py makemigrations
```

**Apply migrations:**
```bash
python manage.py migrate
```

You should see:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, analyzer
Running migrations:
  Applying admin.0001_initial... OK
  ...
```

### Step 6: Create Superuser (Optional)

If you want to access Django admin panel:

```bash
python manage.py createsuperuser
```

Prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: (enter password)

### Step 7: Run Development Server

```bash
python manage.py runserver
```

You should see:
```
Django version 4.2.7
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 8: Open in Browser

```
http://localhost:8000
```

## ✅ Verification Steps

### Check 1: Homepage loads
- [ ] Navigate to http://localhost:8000
- [ ] See "Resume Analyzer" title
- [ ] See feature cards
- [ ] "Start Analyzing" button visible

### Check 2: Upload form
- [ ] Click "Start Analyzing"
- [ ] See file upload area
- [ ] See job description input
- [ ] See "Analyze Resume" button

### Check 3: Admin panel (if superuser created)
- [ ] Navigate to http://localhost:8000/admin
- [ ] Login with superuser credentials
- [ ] See ResumeAnalysis model

## 🧪 Test Analysis

### Sample Resume
Create a file `sample_resume.txt` with:
```
John Doe
Senior Python Developer
Experience:
- 5 years Python development
- Django framework expertise
- PostgreSQL database design
- REST API development
- Docker containerization
- Git version control
```

Convert to PDF using any PDF creator.

### Sample Job Description
Use the job description from README.md

### Expected Result
- Match score: 60-80%
- Matched skills: Python, Django, PostgreSQL, REST, Git, Docker
- Missing skills: AWS, Kubernetes, etc.

## 🐛 Common Issues & Solutions

### Issue 1: "Command 'python' not found"
**Solution:** Use `python3` instead:
```bash
python3 manage.py runserver
```

### Issue 2: "No module named 'django'"
**Solution:** Activate virtual environment and reinstall:
```bash
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
```

### Issue 3: "Port 8000 already in use"
**Solution:** Use different port:
```bash
python manage.py runserver 8001
```

### Issue 4: "Database locked" error
**Solution:** Delete db.sqlite3 and re-migrate:
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue 5: "Permission denied" (Linux/macOS)
**Solution:** Make files executable:
```bash
chmod +x manage.py
```

## 📚 Useful Commands

```bash
# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate          # macOS/Linux

# Deactivate virtual environment
deactivate

# Run server
python manage.py runserver
python manage.py runserver 8001   # Different port

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open shell
python manage.py shell

# Clear database
python manage.py flush

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic
```

## 🚀 Starting Fresh

If you want to reset everything:

```bash
# Deactivate virtual environment
deactivate

# Delete virtual environment
rmdir /s venv                      # Windows
rm -rf venv                        # macOS/Linux

# Delete database
rm db.sqlite3

# Create new virtual environment
python -m venv venv
venv\Scripts\activate              # Windows
source venv/bin/activate          # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Run server
python manage.py runserver
```

## 📖 Documentation Files

- `README.md` - Main project documentation
- `SETUP.md` - This file, detailed setup instructions
- `analyzer/ml_utils.py` - ML algorithm implementation
- `analyzer/views.py` - View logic
- `analyzer/models.py` - Database models

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Scikit-learn Guide](https://scikit-learn.org/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)

## 💡 Tips

1. **Keep virtual environment active** - Always see `(venv)` prefix
2. **Use .env file** - Store sensitive settings
3. **Regular backups** - Backup db.sqlite3 periodically
4. **Check logs** - Terminal shows helpful error messages
5. **Test frequently** - Test after each change

## ✨ You're All Set!

Your Resume Analyzer is ready to use. Start analyzing resumes! 🚀

If you face any issues, check the troubleshooting section or open an issue on GitHub.
