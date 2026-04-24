from pydantic import BaseModel, ConfigDict


class TermoContratualRead(BaseModel):
    """Item do catálogo de termos contratuais (dropdown)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
