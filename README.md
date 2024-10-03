# Dom Explorer

Another OSINT software

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package installer)
- Virtual env (for creating isolated Python environments)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/The-True-Hooha/dom-explorer
    cd dom-explorer
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    Ensure you have SQLite installed. The database will be created automatically when you run the application for the first time.

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    fastapi dev main.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Testing

You can test the application using tools like `curl`, Postman, or directly in your browser.

- handle export to csv
- refactor for mobile
