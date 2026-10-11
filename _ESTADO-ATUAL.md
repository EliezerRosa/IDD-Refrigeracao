# MEMO & ESTADO ATUAL - Projeto IDD Refrigeração (HVAC-R)

**Data da Última Atualização:** 2026-10-11
**Fase Atual:** Alinhamento de Escopo, Arquitetura de Dados & Validação de UX

## 📌 1. O Que Já Foi Construído e Validado
- **Apresentação Técnica do MER (`apresentacao/apresentacao_mer.html`):** Apresentação interativa de 8 slides para desenvolvedores e especialistas em manutenção, detalhando a relação de cada tabela e campo com os objetivos do projeto, zero-rolagem e narração sintética.
- **Apresentação de Alinhamento (`index.html`):** Focada em compliance corporativo e escopo PMOC completo.
- **Nova Proposta Ágil (`proposta_simplificada.html`):** Apresentação mais informal e imersiva para o cliente Renato, com layout de zero-rolagem, narração sintética, e mapeamento claro do "Sai vs Fica".
- **Especificação de Domínio Canônica (`docs/refrigeracao_domain_spec.md`):** Mapeamento estrito das invariantes do negócio de HVAC-R (regras de PMOC, balanço de fluidos, transição de máquina de estados de OS).
- **Modelo Entidade-Relacionamento (MER):** Arquitetura lógica do banco de dados mapeada (via Excalidraw/Mermaid), com isolamento multi-tenant e foco nas entidades-núcleo como `Equipamento`, `Laudo_PMOC` e `Medicao_Tecnica`.

## 🚧 2. Próximos Passos (Pendências Ativas)
1. **Aprovação Final da Proposta Ágil:** Aguardando feedback do cliente Renato sobre a jornada de 5 passos do mecânico.
2. **Setup do Repositório e Infraestrutura:** Subir o código para o repositório remoto e configurar a base do projeto (Front-end e/ou Back-end no Supabase).
3. **Mockups das Telas:** Especificar a interface "Offline-first" para o app do técnico.

## 🛠 3. Decisões Arquiteturais Registradas
- **Banco de Dados (Foco na Máquina):** A entidade central é o Equipamento (`qr_code_id`).
- **Segregação:** O laudo legal (`LAUDO_PMOC`) está intencionalmente separado das medições de ciclo frigorífico (`MEDICAO_TECNICA`).
- **Offline First:** Premissa vital para o aplicativo de campo (mecânicos frequentemente não têm sinal em casas de máquina/câmaras).
