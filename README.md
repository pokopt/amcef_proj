# Posts Backend and Frontend

This project provides a Django backend for managing posts and a simple HTML frontend for interacting with the backend. The backend supports CRUD operations for posts.

## Prerequisites

- Python 3.x
- Docker (optional but recommended)

## Getting Started

### Clone the Repository
```sh
git clone https://github.com/pokopt/amcef_proj.git
cd amcef_proj
```
### Setup Backend

#### Using Docker

1. **Build and Run the Docker Container**
    ```sh
    docker build -t amcef-proj .
    docker run -d -p 8000:8000 amcef-proj
    ```

2. **Run Migrations and Collect Static Files**
    
    Migrations and collect static files are done automatically on container start. If you need to do it by hand:
    ```sh
    docker exec -it <container_id> sh -c "python manage.py migrate && python manage.py collectstatic --noinput"
    ```
#### Without Docker

1. **Create and Activate Virtual Environment**

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. **Install Dependencies**

    pip install -r requirements.txt

3. **Run Migrations and Collect Static Files**

    python manage.py migrate
    python manage.py collectstatic

4. **Run the Server**

    python manage.py runserver

### Frontend

1. **Access Frontend**

    - Open `index.html` in your browser. This file provides a simple interface to interact with the backend.

### API Endpoints
All endpoints are documented by swagger. Open url http://127.0.0.1:8000/swagger/ for swagger doc.
- **Fetch All Posts**

    ```
    GET /api/posts/
    ```

- **Fetch Post by ID**

    ```
    GET /api/posts/<post_id>/
    ```

- **Fetch Posts by User ID**

    ```
    GET /api/posts/by_user/<userId>/
    ```

- **Create Post**

    ```
    POST /api/posts/
    ```

- **Delete Post by ID**

    ```
    DELETE /api/posts/<post_id>/
    ```
