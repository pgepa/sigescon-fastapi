-- Migration: tabela termo_contratual (tipos de termos contratuais)
-- Descrição: opções fixas carregadas do banco para substituir texto livre no contrato

CREATE TABLE IF NOT EXISTS termo_contratual (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    "createdAt" TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_termo_contratual_nome UNIQUE (nome)
);

CREATE INDEX IF NOT EXISTS idx_termo_contratual_nome ON termo_contratual (nome);

COMMENT ON TABLE termo_contratual IS 'Catálogo de tipos de termos contratuais (dropdown)';
COMMENT ON COLUMN termo_contratual.id IS 'Identificador (SERIAL inicia em 1)';
COMMENT ON COLUMN termo_contratual.nome IS 'Nome exibido no sistema (até 50 caracteres)';
COMMENT ON COLUMN termo_contratual."createdAt" IS 'Data/hora de criação (sem timezone)';
COMMENT ON COLUMN termo_contratual."updatedAt" IS 'Data/hora da última atualização (sem timezone)';

-- Atualiza "updatedAt" em todo UPDATE (colunas em camelCase)
CREATE OR REPLACE FUNCTION update_termo_contratual_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW."updatedAt" = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_termo_contratual_updated_at ON termo_contratual;
CREATE TRIGGER trg_termo_contratual_updated_at
    BEFORE UPDATE ON termo_contratual
    FOR EACH ROW
    EXECUTE FUNCTION update_termo_contratual_updated_at();
