# Memória Persistente de Interação — App IDD Refrigeração (RefriFácil)

**Data do Registro:** 08/11/2026  
**Contexto:** Transição da modelagem teórica/industrial para prototipação enxuta, focada em pequenas empresas e autônomos.

---

## 1. Diretriz do Usuário e Decisão Estratégica
* **Solicitação do Usuário:** Reduzir drásticamente o escopo e profundidade, eliminando sobrecargas burocráticas/industriais de PMOC pesados e laudos periciais complexos.
* **Público-Alvo Definido:**
  1. **Residencial:** Splits Hi-Wall, Ar de Janela e geladeiras domiciliares.
  2. **Pequenos Negócios Locais:** Padarias, açougues, mercadinhos e bares (balcões de carnes/frios, freezers comerciais e expositores de bebidas).
* **Mínimo Legal Adotado:** Garantia legal obrigatória de serviço de **90 dias** estipulada pelo Código de Defesa do Consumidor (CDC, art. 26, II).

---

## 2. Artefatos Criados e Estrutura dos Arquivos (`apps_exemplos/refrigeracao_pmoc/`)

### A. Banco de Dados: `schema.sql`
* **Modelo 3 Tabelas:**
  - `clientes`: Identificação se é Residencial ou Comercial, nome, WhatsApp, endereço.
  - `equipamentos`: Relação simplificada de aparelhos vinculados ao cliente.
  - `ordens_servico`: Controle de turno (Manhã, Tarde, Emergencial), queixa/problema, serviço realizado, medições rápidas (°C e PSI), rateio de valores (Peças + Mão de Obra = Total) e prazo de garantia.

### B. Regras de Domínio e Invariantes: `domain_rules.ts`
* **Máquina de Estados:** `ABERTA` -> `EM_ANDAMENTO` -> `CONCLUIDA`.
* **Invariantes Comerciais:** Validação de custos e integridade de relato técnico.
* **Comunicação Direta:** Formatador de mensagem profissional para envio automático via WhatsApp.

### C. Protótipo UI Standalone: `app_refrigeracao.html`
* **Dashboard Dark Mode:** Totalmente autocontido, utilizando `localStorage`.
* **Chaveamento Inteligente:** Altera dinamicamente os tipos de aparelho e valores estimados de mão de obra conforme o segmento (Residencial vs. Comercial).
* **Fluxo Operacional de Campo:**
  1. Abertura da OS em 30 segundos.
  2. Início do atendimento com registro visual no feed.
  3. Modal de conclusão com inserção de parâmetros de teste (°C / PSI) e valor final.
  4. Botão de disparo direto para a API do WhatsApp com mensagem pré-formatada.
  5. Botão de impressão de comprovante físico.
* **Abas Integradas:**
  - *Equipamentos & Negócios:* Monitoramento de máquinas de pequenos comércios.
  - *Termômetro & Diagnóstico:* Calculadora visual de $\Delta T$ ($T_{retorno} - T_{insuflamento}$) para demonstrar eficiência técnica ao cliente.
  - *Faturamento & Garantias:* Relatório de faturamento e listagem de garantias ativas dentro dos 90 dias com reenvio fácil via WhatsApp.

