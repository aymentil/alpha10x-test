# alpha10x-test

## How to use the project

### Create new conda environment
```bash
conda create --name <env_name>
conda activate <env_name>
```

### Install dependencies
```bash
poetry install
```

### Create environment file
```bash
cp server.env.example server.env
```

### Set up environment variable `API_KEY`
Ensure the external service is running in Docker as described in the task.

### Run the FastAPI application
```bash
uvicorn src.main:app --reload
```
### Run tests
```bash
pytest -vv tests
```