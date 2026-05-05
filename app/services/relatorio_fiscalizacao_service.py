import os
import subprocess
from tempfile import NamedTemporaryFile
from docxtpl import DocxTemplate
from app.repositories.relatorio_fiscalizacao_repo import RelatorioRepository
from app.schemas.relatorio_fiscalizacao_schema import RelatorioCreateSchema

class RelatorioService:
    def __init__(self, relatorio_repo: RelatorioRepository):
        self.repo = relatorio_repo
        self.template_path = "templates/template_fiscalizacao.docx"

    # 1. Transformamos em função assíncrona (async)
    # 2. Mudamos o parâmetro para nr_contrato (str)
    async def gerar_pdf(self, nr_contrato: str, dados_form: RelatorioCreateSchema):
        
        # 3. Busca os dados no banco usando await
        dados_banco = await self.repo.get_dados_contrato_completo(nr_contrato)
        
        # 4. Salva o histórico (precisamos do contrato_id que veio do banco)
        await self.repo.salvar_relatorio(dados_banco['contrato_id'], dados_form)

        # Formatação de segurança para datas e valores (caso venham nulos do banco)
        def fmt_date(dt): return dt.strftime('%d/%m/%Y') if dt else ""
        
        valor_global_fmt = ""
        if dados_banco['valor_global']:
            valor_global_fmt = f"R$ {dados_banco['valor_global']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # 5. Monta o contexto (Acesso via dados_banco['campo'])
        contexto = {
            "nr_contrato": dados_banco['nr_contrato'],
            "pae": dados_banco['pae'],
            "objeto": dados_banco['objeto'], # <-- Agora o objeto vai aparecer!
            "data_inicio": fmt_date(dados_banco['data_inicio']),
            "data_fim": fmt_date(dados_banco['data_fim']),
            "valor_global": valor_global_fmt,
            "empresa_nome": dados_banco['empresa_nome'],
            "empresa_cnpj": dados_banco['empresa_cnpj'],
            "fiscal_nome": dados_banco['fiscal_nome'],
            "numero_matricula": dados_banco['numero_matricula'], # <-- Matrícula adicionada
            
            "periodo_de": fmt_date(dados_form.periodo_inicio),
            "periodo_ate": fmt_date(dados_form.periodo_fim),
            "data_relatorio": fmt_date(dados_form.data_relatorio),
            
            # ITEM 1
            "q1s": "X" if dados_form.execucao_objeto_sim else " ",
            "q1n": " " if dados_form.execucao_objeto_sim else "X",
            "execucao_objeto_d": dados_form.execucao_objeto_detalhes,
            
            # ITEM 2
            "q2s": "X" if dados_form.prazo_execucao_sim else " ",
            "q2n": " " if dados_form.prazo_execucao_sim else "X",
            "prazo_execucao_d": dados_form.prazo_execucao_detalhes,

            # ITEM 3
            "q3s": "X" if dados_form.nivel_qualidade_sim else " ",
            "q3n": " " if dados_form.nivel_qualidade_sim else "X",
            "nivel_qualidade_d": dados_form.nivel_qualidade_detalhes,

            # ITEM 4
            "q4s": "X" if dados_form.medicoes_servicos_sim else " ",
            "q4n": " " if dados_form.medicoes_servicos_sim else "X",
            "medicoes_servicos_d": dados_form.medicoes_servicos_detalhes,

            # ITEM 5
            "q5s": "X" if dados_form.ocorrencias_sim else " ",
            "q5n": " " if dados_form.ocorrencias_sim else "X",
            "ocorrencias_d": dados_form.ocorrencias_detalhes,

            # ITEM 6
            "q6s": "X" if dados_form.documentos_habilitacao_sim else " ",
            "q6n": " " if dados_form.documentos_habilitacao_sim else "X",
            "documentos_habilitacao_d": dados_form.documentos_habilitacao_detalhes,

            # ITEM 7
            "q7s": "X" if dados_form.subcontratacao_sim else " ",
            "q7n": " " if dados_form.subcontratacao_sim else "X",
            "subcontratacao_d": dados_form.subcontratacao_detalhes,

            # ITEM 8 (Com 3 opções!)
            "q8s": "X" if dados_form.obrigacoes_empregados_resposta == "sim" else " ",
            "q8n": "X" if dados_form.obrigacoes_empregados_resposta == "nao" else " ",
            "q8a": "X" if dados_form.obrigacoes_empregados_resposta == "na" else " ",
            "obrigacoes_empregados_d": dados_form.obrigacoes_empregados_detalhes,

            # ITEM 9 (Com 3 opções!)
            "q9s": "X" if dados_form.garantias_contratuais_resposta == "sim" else " ",
            "q9n": "X" if dados_form.garantias_contratuais_resposta == "nao" else " ",
            "q9a": "X" if dados_form.garantias_contratuais_resposta == "na" else " ",
            "garantias_contratuais_d": dados_form.garantias_contratuais_detalhes,

            # ITEM 10
            "q10s": "X" if dados_form.execucao_satisfatoria_sim else " ",
            "q10n": " " if dados_form.execucao_satisfatoria_sim else "X",
            "execucao_satisfatoria_d": dados_form.execucao_satisfatoria_detalhes
        }

        # 6. Preenche o DOCX
        doc = DocxTemplate(self.template_path)
        doc.render(contexto)

        # 7. Salva um DOCX temporário
        with NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            doc.save(tmp_docx.name)
            tmp_docx_path = tmp_docx.name

        # 8. Converte para PDF usando LibreOffice
        output_dir = os.path.dirname(tmp_docx_path)
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf",
                tmp_docx_path, "--outdir", output_dir
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro na conversão do LibreOffice: {e.stderr.decode()}")

        pdf_path = tmp_docx_path.replace(".docx", ".pdf")

        # 9. Retorna os caminhos para o router
        return pdf_path, tmp_docx_path