from hashlib import sha256

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from src.dependencias import get_db
from src.models import UsuarioCliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])


class CadastroCliente(BaseModel):
    nome: str = Field(min_length=2, max_length=255)
    email: EmailStr
    telefone: str | None = None
    senha: str = Field(min_length=6, max_length=255)


class LoginCliente(BaseModel):
    email: EmailStr
    senha: str


def hash_senha(senha: str) -> str:
    return sha256(senha.encode("utf-8")).hexdigest()


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
def cadastrar(payload: CadastroCliente, db: Session = Depends(get_db)):
    if db.query(UsuarioCliente).filter(UsuarioCliente.Email == payload.email).first():
        raise HTTPException(status_code=409, detail="Este e-mail já está cadastrado")
    usuario = UsuarioCliente(
        Nome=payload.nome,
        Email=str(payload.email),
        Telefone=payload.telefone,
        Senha=hash_senha(payload.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"id": usuario.id, "nome": usuario.Nome, "email": usuario.Email, "telefone": usuario.Telefone}


@router.post("/login")
def login(payload: LoginCliente, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioCliente).filter(UsuarioCliente.Email == str(payload.email)).first()
    if not usuario or usuario.Senha != hash_senha(payload.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    return {"id": usuario.id, "nome": usuario.Nome, "email": usuario.Email, "telefone": usuario.Telefone}
