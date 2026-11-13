-- ==============================================================================
-- APP REFRIGERAÇÃO SIMPLES (HVAC-R ÁGIL) - ESCOPO ENXUTO
-- Foco: Assistência Técnica Local, Residencial (Splits) e Pequenos Comércios
-- (Padarias, Açougues, Mercadinhos, Bares e Clínicas)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. CLIENTES (Residenciais e Pequenos Negócios)
CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo_cliente VARCHAR(20) NOT NULL CHECK (tipo_cliente IN ('RESIDENCIAL', 'COMERCIAL')),
    nome_razao VARCHAR(120) NOT NULL,
    whatsapp VARCHAR(20) NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    bairro VARCHAR(60),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. APARELHOS / MÁQUINAS CADASTRADAS NO CLIENTE
-- Modelagem simplificada: Split residencial, Balcão refrigerado, Freezer ou Geladeira comercial
CREATE TABLE equipamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    identificacao VARCHAR(80) NOT NULL, -- Ex: 'Split Quarto Casal', 'Balcão de Frios Açougue'
    tipo_aparelho VARCHAR(40) NOT NULL CHECK (tipo_aparelho IN ('SPLIT_RESIDENCIAL', 'BALCAO_REFRIGERADO', 'FREEZER_HORIZONTAL', 'EXPOSITOR_BEBIDAS', 'AR_JANELA')),
    marca VARCHAR(50),
    tipo_gas VARCHAR(20) DEFAULT 'R410A' CHECK (tipo_gas IN ('R410A', 'R32', 'R134a', 'R22', 'R290', 'OUTRO')),
    voltagem VARCHAR(10) DEFAULT '220V',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ORDENS DE SERVIÇO (OS) - FLUXO RÁPIDO DO TÉCNICO
CREATE TABLE ordens_servico (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    equipamento_id UUID REFERENCES equipamentos(id) ON DELETE SET NULL,
    tipo_servico VARCHAR(40) NOT NULL CHECK (tipo_servico IN ('LIMPEZA_HIGIENIZACAO', 'CARGA_DE_GAS', 'CONSERTO_VAZAMENTO', 'TROCA_CAPACITOR_MOTOR', 'INSTALACAO')),
    status VARCHAR(20) NOT NULL DEFAULT 'ABERTA' CHECK (status IN ('ABERTA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA')),
    
    data_visita DATE NOT NULL DEFAULT CURRENT_DATE,
    periodo_visita VARCHAR(15) CHECK (periodo_visita IN ('MANHA', 'TARDE', 'NOITE', 'EMERGENCIAL')),
    
    defeito_reclamado TEXT,              -- "Não gela", "Pingando água dentro", "Fazendo barulho"
    servico_realizado TEXT,              -- "Higienização da evaporadora + desobstrução de dreno"
    
    -- Diagnóstico Prático Essencial (Sem fórmulas complexas)
    temperatura_insuflamento_c NUMERIC(4,1), -- Ex: 11.5 °C (teste rápido de termômetro)
    pressao_gas_psi NUMERIC(5,1),           -- Ex: 120 PSI
    teve_recarga_gas BOOLEAN DEFAULT FALSE,
    
    -- Orçamento e Pagamento Direto
    valor_pecas NUMERIC(10,2) DEFAULT 0.00 CHECK (valor_pecas >= 0),
    valor_mao_de_obra NUMERIC(10,2) NOT NULL DEFAULT 0.00 CHECK (valor_mao_de_obra >= 0),
    valor_total NUMERIC(10,2) GENERATED ALWAYS AS (valor_pecas + valor_mao_de_obra) STORED,
    forma_pagamento VARCHAR(20) CHECK (forma_pagamento IN ('PIX', 'DINHEIRO', 'CARTAO_CREDITO', 'CARTAO_DEBITO', 'A_PRAZO')),
    pago BOOLEAN DEFAULT FALSE,
    
    garantia_dias INT DEFAULT 90 CHECK (garantia_dias >= 0), -- 90 dias padrão CDC
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    concluido_em TIMESTAMPTZ
);
