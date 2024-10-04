# Gym API

A FastAPI-based API for managing gym workouts, users, and subscription plans.

## Features

- User authentication and authorization
- Workout tracking
- Subscription plan management
- Daily automated task to update user subscription status

## Technologies Used

- FastAPI
- SQLAlchemy
- APScheduler
- PostgreSQL (or your database of choice)

## Setup and Installation

1.  Clone the repository:

    -git clone https://github.com/Lucifer203/GymApi.git

    -cd GymApi

2.  Set up a virtual environment:

    python -m venv venv

    source venv/bin/activate

3.  Install dependencies:

    pip install -r requirements.txt

4.  Set up environment variables:
    Create a `.env` file in the root directory and add:

        DATABASE_HOSTNAME=your_database_host
        DATABASE_PORT=your_database_port
        DATABASE_PASSWORD=your_database_password
        DATABASE_NAME=your_database_name
        DATABASE_USERNAME=your_database_username
        SECRET_KEY=your_secret_key
        ALGORITHM=your_algorithm
        ACCESS_TOKEN_EXPIRE_MINUTES=token_expiry_time_in_minutes

5.  Run the application:

    uvicorn main:app --reload
