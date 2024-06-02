# ALLCT_in_Django

This Django project implements a cryptocurrency trading bot that automatically performs trades on the Binance exchange. The bot uses various technical analysis indicators to evaluate trading opportunities and execute trades. It also includes user authentication with JWT for secure access.

## Project History

This project was created to develop an automated trading system using Django Rest Framework (DRF) and Celery for task management. The bot is capable of:

- Evaluating all available coins on Binance and determining which ones are likely to increase in price.
- Automatically buying coins based on evaluation results.
- Selling coins when a desired profit is achieved.
- Monitoring newly added coins and executing trades accordingly.
- Ensuring user authentication through JWT for secure access to the system.

## Features

- User Registration and Login
- JWT Authentication
- Automated Trading Bot using Celery
- Technical Analysis Indicators (RSI, MACD, Bollinger Bands)
- Admin Interface for Bot Configuration and Trade Logs

## Installation

### Prerequisites

- Python 3.10 or later
- Redis (for Celery backend)
- Django 4.0 or later

### Clone the Repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### Setup Virtual Environment

- Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Celery Worker
- Start the Celery worker:

```bash
celery -A trading_bot worker --loglevel=info
```

### Run the Django Development Server

```bash
python manage.py runserver
```

### Usage
- Access the Admin Interface
- - Open your web browser and navigate to:

```bash
http://127.0.0.1:8000/admin
```

#### Log in with the superuser credentials you created earlier. Configure the bot settings in the admin interface.

#### API Endpoints

- Register a new user:

```bash
POST /api/users/register/
```

- Request Body:

```bash
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

- Login a user:

```bash
{
  "username": "testuser",
  "password": "password123"
}
```

- Logout a user:

```bash
POST /api/users/logout/
```

- Request Body:

```bash
{
  "refresh_token": "<refresh_token>"
}
```

### Running the Trading Bot
- The trading bot will run automatically after a successful login. It evaluates coins and performs trades based on predefined criteria.

### Contributing
- If you want to contribute to this project, feel free to fork the repository and submit a pull request.
