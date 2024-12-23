build:
    docker build -t soonish .
serve:
    docker run -p 8002:8000 -v $(pwd):/app/ soonish
up:
    docker compose up --build

down:
    docker compose down 

populate-test-events:
    python scripts/populate_test_events.py
