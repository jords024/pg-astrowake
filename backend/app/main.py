from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from .database import engine, Base, get_db
from .models import Lead
from .schemas import LeadCreate, LeadUpdate, LeadResponse

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'novo';"))
        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS chamado BOOLEAN DEFAULT FALSE;"))
        conn.commit()
    except Exception as e:
        print("Migracao de colunas:", e)

app = FastAPI(title="Astrowake Leads API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Astrowake Leads API"}

@app.post("/api/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def criar_lead(lead_in: LeadCreate, db: Session = Depends(get_db)):
    db_lead = Lead(
        nome=lead_in.nome,
        telefone=lead_in.telefone,
        origem=lead_in.origem or "pg-astrowake",
        url=lead_in.url,
        status="novo",
        chamado=False
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.get("/api/leads", response_model=List[LeadResponse])
def listar_leads(skip: int = 0, limit: int = 200, status_filtro: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Lead)
    if status_filtro:
        query = query.filter(Lead.status == status_filtro.lower())
    leads = query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()
    return leads

@app.patch("/api/leads/{lead_id}", response_model=LeadResponse)
def atualizar_lead(lead_id: int, lead_in: LeadUpdate, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead nao encontrado.")

    if lead_in.status is not None:
        db_lead.status = lead_in.status
        if lead_in.status in ["chamado", "comprou"]:
            db_lead.chamado = True

    if lead_in.chamado is not None:
        db_lead.chamado = lead_in.chamado
        if lead_in.chamado and db_lead.status == "novo":
            db_lead.status = "chamado"

    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.delete("/api/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead nao encontrado.")
    db.delete(db_lead)
    db.commit()
    return None