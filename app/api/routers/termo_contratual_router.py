import asyncpg
from fastapi import APIRouter, Depends
from typing import List

from app.core.database import get_connection
from app.repositories.termo_contratual_repo import TermoContratualRepository
from app.schemas.termo_contratual_schema import TermoContratualRead
from app.api.dependencies import get_current_user
from app.schemas.usuario_schema import Usuario

router = APIRouter(
    prefix="/termo-contratual",
    tags=["Termos contratuais"],
)


def get_repo(conn: asyncpg.Connection = Depends(get_connection)) -> TermoContratualRepository:
    return TermoContratualRepository(conn)


@router.get("/", response_model=List[TermoContratualRead])
async def list_termos_contratuais_slash(
    repo: TermoContratualRepository = Depends(get_repo),
    current_user: Usuario = Depends(get_current_user),
):
    rows = await repo.get_all()
    return [TermoContratualRead(**r) for r in rows]


@router.get("", response_model=List[TermoContratualRead])
async def list_termos_contratuais(
    repo: TermoContratualRepository = Depends(get_repo),
    current_user: Usuario = Depends(get_current_user),
):
    rows = await repo.get_all()
    return [TermoContratualRead(**r) for r in rows]
