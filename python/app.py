from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from service.producer import run_producer

app = FastAPI()

@app.post("/event/import-file")
async def import_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        run_producer(file_content, file.filename)

        return JSONResponse(content={"message": "Arquivo importado com sucesso e enviado para o Kafka"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {e}")