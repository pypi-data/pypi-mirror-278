import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

gui = FastAPI()


def start_server() -> None:
    print("Open your browser and go to http://127.0.0.1:8000")
    print("Press CTRL + C to terminate")
    uvicorn.run(gui, host="127.0.0.1", port=8000, log_level="critical")


templates = Jinja2Templates(directory="templates")


@gui.get("/", response_class=HTMLResponse)
async def homepage(request: Request):  # type: ignore
    # Sample data for the table
    table_data = [
        {"name": "Apple", "invested": 1000, "current": 1200, "performance": "+20%"},
        {"name": "Google", "invested": 1500, "current": 1800, "performance": "+20%"},
        {"name": "Microsoft", "invested": 2000, "current": 2400, "performance": "+20%"},
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "table_data": table_data}
    )
