from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "Astrowake Leads API"}

def test_criar_lead_com_sucesso():
    payload = {
        "nome": "Aryaraj Fernandes",
        "telefone": "5585988146141",
        "origem": "pg-astrowake",
        "url": "http://localhost:8080"
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Aryaraj Fernandes"
    assert data["telefone"] == "5585988146141"
    assert data["status"] == "novo"
    assert data["chamado"] is False
    assert "id" in data
    assert "created_at" in data

def test_rejeitar_lead_com_nome_invalido():
    payload = {
        "nome": "A",
        "telefone": "5585988146141"
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 422

def test_rejeitar_lead_com_telefone_invalido():
    payload = {
        "nome": "Carlos Silva",
        "telefone": "123"
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 422

def test_listar_leads():
    client.post("/api/leads", json={"nome": "Lead 1", "telefone": "5585999990001"})
    client.post("/api/leads", json={"nome": "Lead 2", "telefone": "5585999990002"})

    response = client.get("/api/leads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "Lead 2"
    assert data[1]["nome"] == "Lead 1"

def test_atualizar_status_lead_crm():
    res_create = client.post("/api/leads", json={"nome": "Lead CRM", "telefone": "5585999990003"})
    lead_id = res_create.json()["id"]

    res_patch = client.patch(f"/api/leads/{lead_id}", json={"status": "chamado"})
    assert res_patch.status_code == 200
    data = res_patch.json()
    assert data["status"] == "chamado"
    assert data["chamado"] is True

    res_comprou = client.patch(f"/api/leads/{lead_id}", json={"status": "comprou"})
    assert res_comprou.status_code == 200
    assert res_comprou.json()["status"] == "comprou"

    res_desistiu = client.patch(f"/api/leads/{lead_id}", json={"status": "desistiu"})
    assert res_desistiu.status_code == 200
    assert res_desistiu.json()["status"] == "desistiu"

def test_rejeitar_status_invalido():
    res_create = client.post("/api/leads", json={"nome": "Lead CRM 2", "telefone": "5585999990004"})
    lead_id = res_create.json()["id"]

    res_invalido = client.patch(f"/api/leads/{lead_id}", json={"status": "status_que_nao_existe"})
    assert res_invalido.status_code == 422

def test_deletar_lead():
    res_create = client.post("/api/leads", json={"nome": "Lead Deletar", "telefone": "5585999990005"})
    lead_id = res_create.json()["id"]

    res_delete = client.delete(f"/api/leads/{lead_id}")
    assert res_delete.status_code == 204

    # Verificar que nao existe mais
    res_get = client.get("/api/leads")
    assert len(res_get.json()) == 0