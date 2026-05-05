# app/schemas/relatorio_fiscalizacao_schema.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class RelatorioCreateSchema(BaseModel):
    periodo_inicio: date
    periodo_fim: date
    data_relatorio: date

    # Item 1
    execucao_objeto_sim: bool
    execucao_objeto_detalhes: Optional[str] = ""

    # Item 2
    prazo_execucao_sim: bool
    prazo_execucao_detalhes: Optional[str] = ""

    # Item 3
    nivel_qualidade_sim: bool
    nivel_qualidade_detalhes: Optional[str] = ""

    # Item 4
    medicoes_servicos_sim: bool
    medicoes_servicos_detalhes: Optional[str] = ""

    # Item 5
    ocorrencias_sim: bool
    ocorrencias_detalhes: Optional[str] = ""

    # Item 6
    documentos_habilitacao_sim: bool
    documentos_habilitacao_detalhes: Optional[str] = ""

    # Item 7
    subcontratacao_sim: bool
    subcontratacao_detalhes: Optional[str] = ""

    # Item 8
    obrigacoes_empregados_resposta: str
    obrigacoes_empregados_detalhes: Optional[str] = ""

    # Item 9
    garantias_contratuais_resposta: str
    garantias_contratuais_detalhes: Optional[str] = ""

    # Item 10
    execucao_satisfatoria_sim: bool
    execucao_satisfatoria_detalhes: Optional[str] = ""

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None