### 1. Create and Activate a Virtual Environment

Using a virtual environment is a best practice for managing project-specific dependencies.

```bash
# Create a virtual environment using Python 3.13
python3.13 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

This project requires Google Cloud credentials to be set in an environment file.

First, create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Next, open the newly created `.env` file and fill in the required values for your Google Cloud project.