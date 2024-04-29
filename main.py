from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from fastapi.responses import FileResponse
from fastapi.responses import Response
import pandas as pd
import io 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") 
template = Jinja2Templates(directory="templates")



@app.post("/uploaded/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    try:
        print("Recibiendo archivos...")
        dfs = []  # Lista para almacenar los DataFrames de los archivos
        for file in files:
            print(f"Procesando archivo: {file.filename}")
            contents = await file.read()  # Leer el contenido del archivo
            df = pd.read_excel(io.BytesIO(contents))  # Convertir el contenido a DataFrame
            dfs.append(df)

        # Aquí puedes procesar tus DataFrames como lo necesites
        # Por ejemplo, combinarlos, realizar cálculos, etc.
        # En este ejemplo, simplemente los combinaremos en un solo DataFrame
        combined_df = pd.concat(dfs)

        print("Generando archivo de salida...")
        # Guardar el nuevo DataFrame en un archivo de Excel en memoria
        output_excel = io.BytesIO()
        combined_df.to_excel(output_excel, index=False)
        output_excel.seek(0)

        print("Leyendo contenido del archivo generado en memoria...")
        # Leer el contenido del archivo generado en memoria
        file_content = output_excel.getvalue()

        print("Devolviendo el contenido del archivo como respuesta HTTP...")
        # Devolver el contenido del archivo como una respuesta HTTP con el tipo de contenido adecuado
        return Response(content=file_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment;filename=output.xlsx"})

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/uploadfiles/")
def upload_files(req: Request):
    return template.TemplateResponse(
        name = "uploadfiles.html",
        context= {"request":req}
    )

@app.get("/")
async def login(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

