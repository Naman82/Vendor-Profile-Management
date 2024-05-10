# Vendor Management System

Welcome to the Vendor Management System. This project is designed to  handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Features
- **Vendor Profile Management**: Manage vendors' profiles, through CRUD operations.
- **Purchase Order Tracking**: Track purchase orders.
- **Vendor Performance Evaluation**: Evaluate vendors' work, and track their performance.
- **Real Time Updates**: Used Django signals to update data in real time.

## Getting Started
To get started with the project, follow the steps below to clone the repository, set up a virtual environment, install dependencies, and run the development server.

### Prerequisites
- Python (3.8 or later)
- Git

### Clone the Repository
```bash
git clone 
```

### Set Up a Virtual Environment
```bash
py -m venv env
```

### Activate the Virtual Environment
On Windows:
```bash
env\Scripts\activate
```
On Mac/Linux:
```bash
source env/bin/activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Create a .env file
```
move the content of env.example file inside .env file
SECRET_KEY = "......................................"
```

### Run the Development Server
```bash
py manage.py runserver
```

Once the server is running, you can access the application at http://127.0.0.1:8000/docs in your web browser.
