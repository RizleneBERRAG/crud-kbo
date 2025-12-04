from fastapi import FastAPI

app = FastAPI(title="CRUD KBO")

@app.get("/ping")
def ping():
    return {"message": "pong"}
