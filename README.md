# 🎬 Content Review API

A fully authenticated REST API built using Django REST Framework for managing streaming platforms, artists, multimedia content, and user-submitted reviews.

This backend project supports token-based authentication, secure review submissions, and admin-level control over platform data — all wrapped in clean, filterable, and paginated endpoints.

---

## 🌐 Live Demo

**Base URL:** [`https://content-review.onrender.com`](https://content-review.onrender.com)

> 🔒 All endpoints require a valid token, including `GET` requests.

---

## ✨ Features

- 🔐 Token-based user registration and login
- 🎥 CRUD for streaming content, artists, and platforms
- ✍️ One-review-per-user restriction per content
- 🔎 Advanced filtering and search support
- 🧾 Custom permissions: Admin-only writes & user-owned review control
- 🚦 Request throttling on all resource types

---

## 🚀 Getting Started (Local)

```bash
# Clone the repository
git clone https://github.com/bitsbuild/ContentReviewBackend.git
cd ContentReviewBackend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations and run the dev server
python manage.py migrate
python manage.py runserver
````

---

## 🔑 Authentication

This project uses **Token Authentication** via Django REST Framework.

> 📌 All API requests must include the token in the header — even for GET.

### How to Use Token in Postman

1. After registration or login, copy the token
2. In **Postman**, go to the **Headers** tab
3. Add:

```
Key: Authorization
Value: Token <your_token_here>
```

✅ Example:

```
Authorization: Token 9a14abf7d93a4112345abc...
```

---

## 📫 API Endpoints and Usage

> Base paths:
>
> * `/api/` → content, reviews, artists, platforms
> * `/user/` → register, login, delete

---

### 👤 User Endpoints

#### 🔸 Register

`POST /user/create/`

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "confirm_password": "securepassword"
}
```

Returns:

```json
{
  "status": "Account Created Successfully",
  "token": "<your_token_here>"
}
```

---

#### 🔸 Login (Obtain Token)

`POST /user/token/`

```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

Returns:

```json
{
  "token": "<your_token_here>"
}
```

---

#### 🔸 Delete Account

`POST /user/delete/`
🔒 Requires Token Auth

Deletes the currently authenticated user.

---

### 🎞️ Content Endpoints

#### 🔹 List Content

`GET /api/contents/`
🔒 Requires Token Auth

Supports:

* Pagination: `?page=1`
* Filtering: `?artists=<id>&content_platform=<id>&content_released=true`
* Search: `?search=platform_name` or `?search=artist_name`

---

#### 🔹 Create Content

`POST /api/contents/`
🔒 Admin Only (`is_staff=True`)

```json
{
  "content_name": "Inception",
  "content_description": "Sci-fi thriller",
  "content_released": true,
  "content_platform": "<platform_id>",
  "artists": ["<artist_id_1>", "<artist_id_2>"]
}
```

---

### 🧑‍🎤 Artist Endpoints

`GET /api/artists/`
🔒 Requires Token Auth
🔒 Write Access: Admin Only

```json
{
  "artist_name": "Hans Zimmer",
  "artist_about": "Film Composer"
}
```

Search supported:

```
?search=zimmer
```

---

### 📺 Platform Endpoints

`GET /api/platforms/`
🔒 Requires Token Auth
🔒 Write Access: Admin Only

```json
{
  "platform_name": "Netflix",
  "platform_about": "Streaming service",
  "platform_url": "https://netflix.com"
}
```

Search supported:

```
?search=netflix
```

---

### ✍️ Review Endpoints

`GET /api/reviews/`
🔒 Requires Token Auth

Supports:

* Filtering: `?review_movie=<id>&review_stars=5`
* Search: `?search=Inception`

#### 🔹 Create Review

`POST /api/reviews/`
🔒 Requires Token Auth

```json
{
  "review_name": "Masterpiece!",
  "review_body": "Brilliant visuals and music",
  "review_stars": 5,
  "review_movie": "<content_id>"
}
```

> 📌 Each user can post only one review per content (enforced via DB constraint).

---

## 🔍 Filters & Search

| Endpoint          | Filters                                           | Search Fields                                             |
| ----------------- | ------------------------------------------------- | --------------------------------------------------------- |
| `/api/contents/`  | `artists`, `content_platform`, `content_released` | `artists__artist_name`, `content_platform__platform_name` |
| `/api/artists/`   | —                                                 | `artist_name`, `artist_about`                             |
| `/api/platforms/` | —                                                 | `platform_name`, `platform_about`, `platform_url`         |
| `/api/reviews/`   | `review_movie`, `review_stars`, `review_user`     | `review_movie__content_name`                              |

---

## 🛡️ Permissions Overview

| Resource                    | Read Access      | Write Access                    |
| --------------------------- | ---------------- | ------------------------------- |
| Users (create/token/delete) | Register: Open   | 🔒 Delete: Token Required       |
| Content / Platform / Artist | 🔒 Auth Required | 🔒 Admin Only (`is_staff=True`) |
| Reviews                     | 🔒 Auth Required | 🔒 Only creator can edit/delete |

📌 *All API access is secured via token authentication.*
No anonymous access is allowed — not even for GET requests.

> Admins cannot modify others’ reviews. Review ownership is enforced.

---

## 🚦 Throttling

Custom throttle classes are applied for:

* User actions (create/token/delete)
* Content
* Platforms
* Artists
* Reviews

This ensures fair usage and protects against abuse.

---

## ⚙️ Tech Stack

* **Python 3.10**
* **Django 5.x**
* **Django REST Framework**
* **SQLite** (used in both development and deployment)
* **Render.com** (deployment)
* **Postman** (API testing)

> 📌 Note: This project uses SQLite even on Render. For scalable production usage, integrating PostgreSQL is recommended.

---

## 🪪 License

This project is released under the [MIT License](LICENSE).

---
