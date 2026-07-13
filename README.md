# Placement Portal application v2 (MAD-II Project)

A **role-based web application** developed using **Flask** and **Vue 3** that streamlines campus placement activities by enabling structured interaction between **Admin (Institute Placement Cell), Companies,** and **Students**.

The application replaces manual processes such as spreadsheets and emails with a centralized system for managing company **approvals, placement drives, student applications, and placement history**.

## Tech Stack

- **Backend:** Flask (Python), celery(Async jobs), Redis(Cache, Message broker, Results backend), Jinja2 (Report templates)
- **Database:** SQLite + SQLAlchemy ORM
- **Frontend:** Vue3, Vue Router
- **Styling:** Bootstrap 5, Bootstrap Icons, CSS
- **Build Tool** Vite

## Features

### Student

- Register and login
- Update student profile
- View available company drives
- Apply to drives
- Track application status
- View application history
- Receive notifications on status changes
- Export CSV reports (assignments)

### Admin

- Manage companies, drives and students
- View student applications
- Update application status
- Monitor activity
- Receive monthly reports (mail)

### Company

- Provide company details (profile)
- Create placement drives (if allowed)
- Define eligibility criteria
- View applicants for their drives
- Select / Reject / Shortlist candidates
- Manage Interviews
- Create Placement records
- Export CSV reports (assignments)

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/24f2009067/placement-portal-application-v2.git
cd placement-portal-application-v2

```

### 2. install dependencies

```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm i
```

### 3. Install and start Redis

Celery (broker + result backend) and Flask-Caching both depend on Redis running locally on the default port.

```bash
# macOS (Homebrew)
brew install redis && brew services start redis

# Ubuntu/Debian
sudo apt install redis-server && sudo systemctl start redis-server

# Windows: use WSL, or run via Docker:
docker run -d -p 6379:6379 redis
```

### 4. Create `.env` files

`frontend/.env`

```bash
VITE_API_URL=http://localhost:5000
```

`backend/.env`

```bash
MAIL_USERNAME=
MAIL_PASSWORD=
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

`MAIL_USERNAME` / `MAIL_PASSWORD` are used for sending notification emails (interview reminders, reports). If using Gmail, generate an App Password rather than your regular account password.

> **Note:** Admin Email: admin@ppa.com, Default password: password

### 5. Start the app
```bash
# backend/ - Flask API server
python app.py

# backend/ - Celery worker (processes async tasks: reports, emails)
celery -A app.celery worker -l info

# backend/ - Celery beat (schedules recurring tasks: interview reminders, monthly placement report, auto-closing expired drives)
celery -A app.celery beat -l info

# frontend/ - Vite dev server
npm run dev
```

> The API will be available at http://localhost:5000 and the frontend at the port Vite prints (typically http://localhost:5173).

> **Note:** The app was only tested on "linux". The app should run on macOS and windows (WSL)

## Project Structure

```
placement-portal-application-v2/
├── backend
│   ├── app.py
│   ├── celerybeat-schedule
│   ├── extensions.py
│   ├── init_cache.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routes
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── company.py
│   │   └── student.py
│   ├── seed.py
│   ├── tasks.py
│   ├── templates
│   │   └── adminReport.html
│   ├── validator.py
│   └── workers.py
├── frontend
│   ├── eslint.config.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── recruitx
│   │       ├── recruitex-default-monochrome-black.svg
│   │       ├── recruitex-default-monochrome.svg
│   │       └── recruitex-default-monochrome-white.svg
│   ├── src
│   │   ├── api
│   │   │   ├── admin.js
│   │   │   ├── auth.js
│   │   │   ├── company.js
│   │   │   ├── student.js
│   │   │   └── utility.js
│   │   ├── App.vue
│   │   ├── components
│   │   │   ├── admin
│   │   │   │   ├── AdminDashboard.vue
│   │   │   │   ├── ApplicationCard.vue
│   │   │   │   ├── ApplicationSection.vue
│   │   │   │   ├── CompanySection.vue
│   │   │   │   ├── DashboardStats.vue
│   │   │   │   ├── DriveCard.vue
│   │   │   │   ├── DriveSection.vue
│   │   │   │   └── StudentSection.vue
│   │   │   ├── company
│   │   │   │   ├── ApplicationCard.vue
│   │   │   │   ├── ApplicationSection.vue
│   │   │   │   ├── CompanyDashboard.vue
│   │   │   │   ├── CompanyProfile.vue
│   │   │   │   ├── CreateDrive.vue
│   │   │   │   ├── DriveDetail.vue
│   │   │   │   ├── DriveSection.vue
│   │   │   │   └── UpdateDrive.vue
│   │   │   ├── shared
│   │   │   │   ├── AppNavbar.vue
│   │   │   │   └── ToastContainer.vue
│   │   │   └── student
│   │   │       ├── ApplicationSection.vue
│   │   │       ├── CompanyDetails.vue
│   │   │       ├── CompanySection.vue
│   │   │       ├── DriveCard.vue
│   │   │       ├── HistoryPage.vue
│   │   │       ├── NotificationPage.vue
│   │   │       ├── StudentDashboard.vue
│   │   │       └── StudentProfile.vue
│   │   ├── main.js
│   │   ├── router
│   │   │   └── index.js
│   │   ├── toast.js
│   │   └── views
│   │       ├── AdminView.vue
│   │       ├── AuthView.vue
│   │       ├── CompanyView.vue
│   │       └── StudentView.vue
│   └── vite.config.js
└── README.md

16 directories, 64 files
```

## Author

Prajin GN (24f2009067)
