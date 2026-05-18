# MusicBackend 🎵

A **Digital Music Publishing & Promotion Platform** built with Django and Django REST Framework. Artists can upload songs, pay for promotion, and get their music approved by admins for public listening.

---

## 🚀 Features

### Public Users
- Browse approved songs
- View trending music
- Search music (coming soon)

### Artists
- Register and login
- Upload songs (audio + cover image)
- Pay via Airtel Money, Mpamba, or Bank
- Track their uploaded songs
- Manual payment verification system

### Admin
- Approve/Reject artists
- Approve/Reject songs
- Verify payments
- Full content management via Django Admin

---

## 🛠 Tech Stack

- **Backend**: Django 5+
- **API**: Django REST Framework + SimpleJWT
- **Database**: SQLite (can be changed to PostgreSQL)
- **Authentication**: JWT Tokens
- **File Handling**: Images & Audio uploads
- **Frontend Ready**: CORS enabled

---

## 📁 Project Structure

```bash
musicbackend/
├── musicbackend/          # Main project settings
├── artists/               # Artist registration & profiles
├── songs/                 # Song upload & management
├── payments/              # Payment proof handling
├── coreapi/               # Public APIs
├── media/                 # Uploaded files (songs, covers, proofs)
├── manage.py
├── README.md
└── venv/