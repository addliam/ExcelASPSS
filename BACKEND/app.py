from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import io
import json
from excelaspss import ExcelASPSS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Configuracion(BaseModel):
    items_total_variable1: int
    items_total_variable2: int
    explorar_dimensiones_de_v1: bool
    cantidad_item_por_dimensiones: list[int]
    numero_maximo_de_escala: int

@app.post("/procesar")
async def procesar_excel(
    config: str = Form(...),
    file: UploadFile = File(...)
):
    # Convertir string JSON a modelo Pydantic
    config_dict = json.loads(config)
    config_obj = Configuracion(**config_dict)

    # Leer Excel con pandas
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    procesadorExcelASPSS = ExcelASPSS()
    df_procesado = procesadorExcelASPSS.procesar(dataframe=df,
                                  items_total_variable1=config_obj.items_total_variable1, 
                                  items_total_variable2=config_obj.items_total_variable2, 
                                  explorar_dimensiones_de_v1=config_obj.explorar_dimensiones_de_v1, 
                                  cantidad_item_por_dimensiones=config_obj.cantidad_item_por_dimensiones, 
                                  numero_maximo_de_escala=config_obj.numero_maximo_de_escala)

    # Convertir a CSV en memoria
    output = io.StringIO()
    df_procesado.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=resultado.csv"
        }
    )