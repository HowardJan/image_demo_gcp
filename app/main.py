from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import openai
import uuid
from .gcs_utils import upload_to_gcs

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

openai.api_key = "你的_OPENAI_API_KEY"

@app.get("/", response_class=HTMLResponse)
async def form_post(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def upload_and_analyze(request: Request, file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = f"{uuid.uuid4()}.jpg"
    public_url = upload_to_gcs(file_bytes, filename)

    prompt = f"請幫我分析這張圖片的內容：{public_url}"
    chat_response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": public_url}}]}
        ],
        max_tokens=500
    )

    result = chat_response.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
