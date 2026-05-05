from asyncpg import Connection
from fastapi import HTTPException
from app.schemas.relatorio_fiscalizacao_schema import RelatorioCreateSchema

class RelatorioRepository:
    def __init__(self, db: Connection):
        self.db = db

    async def get_dados_contrato_completo(self, nr_contrato: str):
        # A consulta SQL usa LEFT JOIN (equivalente ao outerjoin)
        # O $1 é a forma como o asyncpg protege contra SQL Injection
        query = """
            SELECT 
                c.id AS contrato_id,
                c.nr_contrato,
                c.pae,
                c.objeto,
                c.data_inicio,
                c.data_fim,
                c.valor_global,
                emp.nome AS empresa_nome,
                emp.cnpj AS empresa_cnpj,
                u.nome AS fiscal_nome,
                u.matricula AS numero_matricula
            FROM contrato c
            LEFT JOIN contratado emp ON c.contratado_id = emp.id
            LEFT JOIN usuario u ON c.fiscal_id = u.id
            WHERE c.nr_contrato = $1
        """
        
        # fetchrow retorna exatamente 1 linha do banco (como um dicionário)
        resultado = await self.db.fetchrow(query, nr_contrato)

        if not resultado:
            raise HTTPException(status_code=404, detail="Contrato não encontrado no banco de dados.")

        return resultado

    async def salvar_relatorio(self, contrato_id: int, dados: RelatorioCreateSchema):
        try:
            # Pega os dados do formulário ignorando o que não foi preenchido
            dados_dict = dados.model_dump(exclude_unset=True)
            
            # Monta o INSERT dinamicamente para todos os itens do formulário
            colunas = ["contrato_id"] + list(dados_dict.keys())
            valores = [contrato_id] + list(dados_dict.values())
            
            # Gera os marcadores do asyncpg ($1, $2, $3...)
            marcadores = ", ".join([f"${i+1}" for i in range(len(valores))])
            nomes_colunas = ", ".join(colunas)
            
            query = f"INSERT INTO relatorio_fiscalizacao ({nomes_colunas}) VALUES ({marcadores}) RETURNING id"
            
            novo_id = await self.db.fetchval(query, *valores)
            return novo_id
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")