# Konnectia - College Social Network

Konnectia is a Django-based social networking platform designed for college communities. It allows students and faculty to connect, share posts, follow each other, and interact in a secure, campus-focused environment.

## Features

- **User Authentication:** Secure registration, login, and logout for users.
- **Profile Management:** Each user has a customizable profile with profile picture, bio, and personal details.
- **Post Creation:** Users can create posts with text and images.
- **Feed:** View all posts, posts from followed users, and saved posts.
- **Follow System:** Follow and unfollow other users to personalize your feed.
- **Like & Save:** Like and save posts for later viewing.
- **Comments:** Comment on posts and engage in discussions.
- **Suggestions:** Discover new people to connect with through smart suggestions.
- **Media Uploads:** Upload and display profile pictures and post images.
- **Pagination:** Efficiently browse posts with pagination.
- **API Support:** REST API endpoints for integration and future expansion.
- **Responsive Design:** User-friendly interface for both desktop and mobile.

## Technologies Used

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (with Django templates)
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Other:** Bootstrap, CORS headers

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/konnectia.git
    cd konnectia
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Mac/Linux
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (admin):**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the app:**
    - Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Project Structure

```
konnectia/
├── authentication/      # User authentication app
├── mainpage/            # Main social features (posts, profiles, etc.)
├── api/                 # REST API endpoints
├── static/              # Static files (CSS, JS, images)
├── media/               # Uploaded media files
├── templates/           # HTML templates
├── konnectia/           # Project settings and URLs
└── manage.py
```

## Configuration

- **Media files:** Uploaded images are stored in the `media/` directory.
- **Static files:** Place custom CSS/JS in the `static/` directory.
- **Settings:** Adjust `settings.py` for database, email, and other configurations.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.

---

**Konnectia** – Connect, share, and grow your college community!