Perfect 👌 Here’s a solid **README.md draft** you can drop into your `Alx_DjangoLearnLab/social_media_api` repo.

---

# Social Media API

A backend API built with **Django** and **Django REST Framework (DRF)** that provides user authentication and profile management for a social media platform.

---

## 🚀 Features

* Custom `User` model with:

  * `bio`
  * `profile_picture`
  * `followers` (Many-to-Many self-relationship)
* Token-based authentication (DRF Token Auth)
* Endpoints for:

  * User registration
  * User login
  * Profile retrieval and update

---

## ⚙️ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

(If `requirements.txt` is not yet created, install manually:)

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 4. Create Superuser (optional for admin panel)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Your API is now running at: `http://127.0.0.1:8000/`

---

## 🔑 Authentication & Usage

This project uses **Token Authentication**. After registering or logging in, you’ll receive a token that must be included in request headers.

**Example Header:**

```
Authorization: Token your_token_here
```

---

## 📡 API Endpoints

### 1. Register

**POST** `/api/auth/register/`

**Request:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword123"
}
```

**Response:**

```json
{
  "user": {
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "a1b2c3d4e5f6..."
}
```

---

### 2. Login

**POST** `/api/auth/login/`

**Request:**

```json
{
  "username": "john_doe",
  "password": "strongpassword123"
}
```

**Response:**

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null,
    "followers": []
  },
  "token": "a1b2c3d4e5f6..."
}
```

---

### 3. Profile

**GET/PUT** `/api/auth/profile/`

* Requires authentication header.
* Retrieve or update the logged-in user’s profile.

**Example Request (PUT):**

```json
{
  "bio": "Backend Engineer",
  "profile_picture": null
}
```

---

## 👤 User Model Overview

The custom user model extends `AbstractUser` and includes:

```python
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
```

---

## 📂 Project Structure

```
social_media_api/
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
└── manage.py
```

---

## 📝 Notes

* Ensure you run migrations **before** creating users.
* Use Postman or cURL to test API endpoints.
* Future features (posts, comments, likes) will build on this foundation.


