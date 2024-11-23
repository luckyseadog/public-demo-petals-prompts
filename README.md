# Petals Prompts Service

***Please, note that this repository is a replica of Petals Prompts private project in GitHub.***

## How to run Backend Server

```
cd app
uvicorn app.main:app --host 0.0.0.0 --port 8075
```

## How to run Frontend Server

```
cd frontend
python -m http.server --bind localhost 8933 -d .
```
