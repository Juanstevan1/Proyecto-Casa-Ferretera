from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from typing import Annotated
from Functions.login import login as lg, Selfromdb
import pandas as pd
import openpyxl
import io
from Functions.DataFunctions import extracting_data
from pymongo import MongoClient, DESCENDING

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

@app.post("/uploaded")
async def create_upload_files(files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]):
    try:
        print("Recibiendo archivos...")
        dfs = []
        for file in files:
            print(f"Procesando archivo: {file.filename}")
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            dfs.append(df)

        new_df, old, new = extracting_data(dfs[0], dfs[1], dfs[2])
        client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')
        db = client["Casa"]
        collection1 = db["Statistics"]
        records = new_df.to_dict(orient='records')
        result = collection1.insert_many(records)
        print(f'Inserted {len(result.inserted_ids)} records')
        client.close()

        output_excel = io.BytesIO()
        new_df.to_excel(output_excel, index=False)
        output_excel.seek(0)
        file_content = output_excel.getvalue()

        return Response(content=file_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment;filename=output.xlsx"})
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uploadfiles")
def upload_files(req: Request):
    return template.TemplateResponse(name="uploadfiles.html", context={"request": req})

@app.get("/main")
async def read_root(req: Request):
    location = req.cookies.get('extra_param')
    values = await Selfromdb(location)
    return template.TemplateResponse(name="component.html", context={"request": req, "plot_data": values})

@app.get("/")
async def login(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

@app.post("/Login")
async def handle_login(request: Request):
    body = await request.body()
    decoded_body = body.decode("utf-8")
    form_data = {}
    for item in decoded_body.split("&"):
        key, value = item.split("=")
        form_data[key] = value
    username = form_data.get("username", "")
    password = form_data.get("password", "")

    username = username.replace('+', " ")
    login = await lg(username, password)
    if login:
        response = RedirectResponse(url="/main", status_code=303)
        if login == "Admin":
            response = RedirectResponse(url="/uploadfiles", status_code=303)
        response.set_cookie(key="extra_param", value=login)
        return response
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
