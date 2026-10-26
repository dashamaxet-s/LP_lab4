# FastAPI REST Service & HTTPX Client

A RESTful API service built with FastAPI for managing items, complete with a robust HTTP client built on httpx.

## Project Structure

```
lab_4_fastapi/
├── src/
│   ├── api_service/      # Server-side code
│   │   ├── models.py     # Pydantic models (ItemCreate, ItemRead)
│   │   ├── repository.py # JSON storage layer
│   │   └── app.py        # FastAPI routes & endpoints
│   └── api_client/       # Client-side code
│       └── client.py     # httpx client with error handling
├── tests/
│   └── test_api.py       # Pytest test suite
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone git@github.com:dashamaxet-s/lab_4_fastapi.git
   cd lab_4_fastapi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI server with auto-reload:
```bash
uvicorn api_service.app:app --reload
```

Once running, you can access:
- **API base URL:** `http://127.0.0.1:8000`
- **Interactive Swagger UI (Auto-documentation):** `http://127.0.0.1:8000/docs`

## Running the Client

With the server running in a separate terminal, you can execute the client script:
```bash
python -m api_client.client
```
*(Note: Ensure you have a `if __name__ == "__main__":` block in `client.py` if you want to run it directly, or use it in a Python script as shown in the code).*

## Running Tests

We use `pytest` for testing. The tests use an isolated temporary repository so your `data.json` won't be polluted.

```bash
pytest -v
```

## API Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|--------------|
| POST   | `/items` | Create a new item | 201, 422 |
| GET    | `/items` | List items (limit/offset) | 200 |
| GET    | `/items/search` | Search items by name | 200 |
| GET    | `/items/{item_id}` | Get a single item | 200, 404 |
| PUT    | `/items/{item_id}` | Update an item | 200, 404, 422 |
| DELETE | `/items/{item_id}` | Delete an item | 204, 404 |