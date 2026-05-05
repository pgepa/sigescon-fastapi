from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from asyncpg import Connection # <-- Importe o Connection
import os

from app.core.database import get_connection # <-- Injetamos a conexão individual
from app.schemas.relatorio_fiscalizacao_schema import RelatorioCreateSchema
from app.repositories.relatorio_fiscalizacao_repo import RelatorioRepository
from app.services.relatorio_fiscalizacao_service import RelatorioService

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

def cleanup_files(*file_paths):
    for path in file_paths:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

@router.post("/gerar-pdf/{nr_contrato:path}")
async def gerar_relatorio_pdf(
    nr_contrato: str, 
    dados_form: RelatorioCreateSchema, 
    background_tasks: BackgroundTasks,
    db: Connection = Depends(get_connection) # <-- Aqui acontece a mágica
):
    try:
        repo = RelatorioRepository(db)
        service = RelatorioService(repo)
        
        # Adicionado o AWAIT na chamada do serviço
        pdf_path, docx_path = await service.gerar_pdf(nr_contrato, dados_form)

        background_tasks.add_task(cleanup_files, pdf_path, docx_path)

        nome_seguro = nr_contrato.replace("/", "-")
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"Fiscalizacao_{nome_seguro}.pdf"
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar o PDF: {str(e)}")