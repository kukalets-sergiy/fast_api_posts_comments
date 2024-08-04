# fast_api_posts_comments

## Description.

This is a API project for managing posts and comments with AI moderation and auto-response.

# Task Description
User Registration
User Login
API for managing posts
API for managing comments
Check for profanity and abuse in posts or comments at the time of creation and block such posts or comments.
Analytics on the number of comments added to posts over a specific period. Example URL: /api/comments-daily-breakdown?date_from=2020-02-02&date_to=2022-02-15. The API should return aggregated analytics per day, including the number of created comments and the number of blocked comments.
Automatic reply to comments if enabled by the user for their posts. The automatic reply should not be immediate but after a period configured by the user. The reply should also be relevant to the post and the comment it is replying to.

## Project Setup

### Clone the repository
git clone https://github.com/kukalets-sergiy/fast_api_posts_comments
cd fast_api_posts_comments
Create a virtual environment (if needed)

python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Configuration
Copy env_example to .env:

cp env_example .env
Generate and add secrets to .env:

# Generate secrets in the terminal
In your terminal:
openssl rand -hex 64
openssl rand -hex 64

SECRET_KEY=$(openssl rand -hex 64)
JWT_SECRET_KEY=$(openssl rand -hex 64)
API_KEY="your_actual_api_key_here" # See the instructions below for obtaining this key

# Update the .env file

Example .env:

SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
API_KEY=your_actual_api_key_here

DATABASE_URL=postgresql://sergiy:fastapi@db:5432/fastapi_project_db

POSTGRES_USER=sergiy
POSTGRES_PASSWORD=fastapi
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_project_db

PGADMIN_DEFAULT_EMAIL=postgres1@gmail.com
PGADMIN_DEFAULT_PASSWORD=fastapi
PGADMIN_LISTEN_PORT=5050

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Obtain API Key for Perspective API
Sign up and create a project:

Go to Google Cloud Console.
Create a new project.
Enable Perspective API:

In the Google Cloud Console, navigate to APIs & Services > Library.
Search for "Perspective API" and enable it.
Create API Key:

Go to APIs & Services > Credentials.
Click on "Create credentials" and select "API key".
Copy the generated API key and add it to your .env file as API_KEY.

# Run the project with Docker
Build and run containers:

docker-compose up --build

# Apply database migrations:
docker-compose exec app alembic upgrade head

# Usage
Go to http://127.0.0.1:8000/docs

User Registration
Perform a POST request to /auth/register with the following JSON data:

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}

User Login
Perform a POST request to /auth/login with the following JSON data:

{
  "username": "testuser",
  "password": "password123"
}

Create a Post
Perform a POST request to /posts/ with the following JSON data and an authentication token:

{
  "title": "New Post",
  "content": "This is the content of the new post."
}

Create a Comment
Perform a POST request to /comments/ with the following JSON data and an authentication token:

{
  "post_id": 1,
  "content": "This is a comment."
}

# Running Tests
(register at least one user)
To run tests, execute the following command:

docker-compose run --rm test


Technologies Used
FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
SQLAlchemy: The Python SQL toolkit and Object-Relational Mapping (ORM) library.
Alembic: A lightweight database migration tool for SQLAlchemy.
Celery: An asynchronous task queue/job queue based on distributed message passing.
Redis: An open-source, in-memory data structure store, used as a database, cache, and message broker.
Docker: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.
Google Perspective API: Uses machine learning models to score the perceived impact a comment might have on a conversation.

For detailed instructions on setting up and running the project, please refer to the above sections.


This `README.md` includes instructions for obtaining the Perspective API key and provides a structured setup guide for the project in English.