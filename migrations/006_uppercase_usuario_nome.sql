-- Migration: normaliza nomes de usuários para CAIXA ALTA
-- Descrição: converte todos os valores de usuario.nome para UPPER(TRIM(nome))

UPDATE usuario
SET
    nome = UPPER(TRIM(nome)),
    updated_at = CURRENT_TIMESTAMP
WHERE
    nome IS NOT NULL
    AND nome <> UPPER(TRIM(nome));
