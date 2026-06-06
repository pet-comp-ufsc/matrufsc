from fastapi import FastAPI, BackgroundTasks, HTTPException
from .crawler import fetch_data
from .parser import parse_to_dict
import os
import json

app = FastAPI(title="CAGR Horários API")

DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/horarios/{semestre}")
async def get_horarios(semestre: str):
    """Retorna os dados cacheados ou erro se não existirem."""
    cache_file = os.path.join(DATA_DIR, f"{semestre}.json")
    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    
    raise HTTPException(
        status_code=404, 
        detail="Dados não encontrados. Use /atualizar/{semestre} primeiro."
    )

@app.post("/atualizar/{semestre}")
async def trigger_update(semestre: str, background_tasks: BackgroundTasks):
    """Dispara a atualização em segundo plano."""
    
    def process_task():
        # Cria pasta temporária para XMLs
        temp_xml_dir = f"./temp_{semestre}"
        os.makedirs(temp_xml_dir, exist_ok=True)
        
        # Executa Crawler -> Parser
        # xmls = fetch_data(semestre, temp_xml_dir)
        dados = parse_to_dict(["/app/data/20261_ARA.xml", "/app/data/20261_BLN.xml", "/app/data/20261_CBS.xml", "/app/data/20261_FLO.xml", "/app/data/20261_JOI.xml"])
        
        # Salva o JSON final (Cache)
        with open(os.path.join(DATA_DIR, f"{semestre}.json"), "w") as f:
            json.dump(dados, f, ensure_ascii=False)

    background_tasks.add_task(process_task)
    return {"message": f"Atualização para {semestre} iniciada em background."}

@app.get("/health")
async def health_check():
    return {"status": "online", "environment": "Debian Sid"}