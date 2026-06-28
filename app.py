from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from processor import process_image

from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from processor import process_image
app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)
BASE_DIR = Path(__file__).parent

templates = Jinja2Templates(
    directory="templates"
)

UPLOAD_DIR = BASE_DIR / "static" / "uploads"
OUTPUT_DIR = BASE_DIR / "static" / "outputs"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.post("/upload")
async def upload_file(
        request: Request,
        file: UploadFile = File(...)
):

    input_path = UPLOAD_DIR / file.filename

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    output_path = (
            OUTPUT_DIR /
            f"processed_{file.filename}.jpg"
    )

    process_image(
        str(input_path),
        str(output_path)
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result_image": f"/static/outputs/{output_path.name}"
        }
    )