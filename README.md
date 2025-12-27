# herdknowledge-app
This contains all of the application code for HerdKnowledge.com



# Development

## Local Development Setup

### Prerequisites
- Python 3.8 or higher

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
Start the FastAPI server using uvicorn:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`
