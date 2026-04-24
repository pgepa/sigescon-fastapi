-- Seed: registros iniciais da tabela termo_contratual
-- Idempotente: pode ser executado mais de uma vez sem duplicar nomes

INSERT INTO termo_contratual (nome) VALUES
    ('Acordo de cooperação'),
    ('Apostilamento'),
    ('Contrato'),
    ('Convênio'),
    ('Termo aditivo'),
    ('Termo de cessão de uso'),
    ('Termo de comodato'),
    ('Termo de cooperação técnica'),
    ('Termo de execução descentralizada'),
    ('Termo de rescisão')
ON CONFLICT (nome) DO NOTHING;
