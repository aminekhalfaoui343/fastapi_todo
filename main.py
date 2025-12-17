import uuid
import logging
import time

from fastapi import Depends, FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import create_todo, delete_todo, get_todo, get_todos, update_todo

# -------------------------
# Logging configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("fastapi-app")

# -------------------------
# Database & App
# -------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

logger.info("FastAPI application starting")

# -------------------------
# DB dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Request logging middleware
# -------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration_ms={duration}"
    )
    return response

# -------------------------
# Routes
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    todos = get_todos(db, session_key)

    logger.info(f"Fetched {len(todos)} todos for session {session_key}")

    context = {
        "request": request,
        "todos": todos,
        "title": "Home"
    }
    response = templates.TemplateResponse("home.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)
    return response


@app.post("/add", response_class=HTMLResponse)
def post_add(request: Request, content: str = Form(...), db: Session = Depends(get_db)):
    session_key = request.cookies.get("session_key")
    todo = create_todo(db, content=content, session_key=session_key)

    logger.info(f"Todo created id={todo.id} session={session_key}")

    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/item.html", context)


@app.get("/edit/{item_id}", response_class=HTMLResponse)
def get_edit(request: Request, item_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db, item_id)

    logger.info(f"Edit page opened for todo id={item_id}")

    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/form.html", context)


@app.put("/edit/{item_id}", response_class=HTMLResponse)
def put_edit(request: Request, item_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    todo = update_todo(db, item_id, content)

    logger.info(f"Todo updated id={item_id}")

    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("todo/item.html", context)


@app.delete("/delete/{item_id}", response_class=Response)
def delete(item_id: int, db: Session = Depends(get_db)):
    delete_todo(db, item_id)

    logger.warning(f"Todo deleted id={item_id}")

    return Response(status_code=204)

# -------------------------
# Test error endpoint (for ELK)
# -------------------------
@app.get("/error")
def error():
    logger.error("Intentional test error triggered")
    raise Exception("Test error for logging")