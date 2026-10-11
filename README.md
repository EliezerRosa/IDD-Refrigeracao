# Gestão de Refrigeração (HVAC-R) & PMOC — Projeto IDD

Projeto de aplicativo para gerência e gestão de serviços de manutenção técnica, preventiva e corretiva na área de **Refrigeração Comercial, Industrial e Climatização (HVAC-R)**, em conformidade com normas regulatórias (**PMOC - Lei 13.589/2018** e **Portaria MS 3.523/1998**).

---

## 📂 Estrutura do Projeto

* 📄 **[`docs/refrigeracao_domain_spec.md`](docs/refrigeracao_domain_spec.md)**  
  Especificação canônica de domínio:
  - Intenções do negócio (técnica, cliente, auditoria)
  - Invariantes e regras rígidas (vácuo em mícrons, balanço de fluidos, trava PMOC, foto antes/depois, assinatura digital)
  - Modelo relacional (Contratos, Equipamentos, Ordens de Serviço, Laudos)
  - Modos Online / Offline First

* 📄 **[`docs/apresentacao_alinhamento_refrigeracao.md`](docs/apresentacao_alinhamento_refrigeracao.md)**  
  Documento de alinhamento estratégico com o cliente para validação de escopo, contexto proposto vs. alternativo e dimensionamento de MVP.

* 🌐 **[`apresentacao/apresentacao_mer.html`](apresentacao/apresentacao_mer.html)** ⭐ **[NOVA - EQUIPE DEV & TÉCNICA]**  
  Apresentação interativa do Modelo Entidade-Relacionamento (MER) para Desenvolvedores e Especialistas de Manutenção:
  - Foco na relação direta entre cada tabela/dado e as metas reais de negócio
  - Layout de **zero rolagem**, painéis glassmorphic, visual de esquemas com PKs/FKs e badges de papéis (Dev vs. Técnico)
  - Narração com voz sintética em português, legendas automáticas e atalhos de teclado
  - Acesso local: `http://localhost:8085/apresentacao_mer.html`

* 🌐 **[`apresentacao/proposta_simplificada.html`](apresentacao/proposta_simplificada.html)**  
  Apresentação interativa da Nova Proposta Ágil e Informal para o cliente Renato:
  - Layout calibrado para **zero rolagem** (100% visível na tela sem barra de scroll)
  - Narração com voz sintética em português e legendas em tempo real
  - Comparativo "Sai vs. Fica", 4 intenções essenciais, invariantes flexibilizadas e fluxo do mecânico em 5 passos
  - Acesso local: `http://localhost:8085/proposta_simplificada.html`

* 🌐 **[`apresentacao/index.html`](apresentacao/index.html)**  
  Apresentação inicial de alinhamento com escopo corporativo e PMOC formal:
  - Narração com voz sintética em português (modo contínuo e pausado)
  - Legendas em tempo real (*closed caption*)
  - Diagramas técnicos de ciclo frigorífico e fluxo de atendimento em campo estilo Excalidraw

---

## 🚀 Como Executar as Apresentações Localmente

Para abrir a apresentação com áudio no navegador:
```powershell
cd "C:\Antigravity - IDD Refrigeração\apresentacao"
python -m http.server 8085
```
E acesse no navegador:
- Apresentação Técnica do MER (Dev + Manutenção): **`http://localhost:8085/apresentacao_mer.html`**
- Nova Proposta Simplificada (Cliente Renato): **`http://localhost:8085/proposta_simplificada.html`**
- Apresentação Anterior (Escopo Formal): **`http://localhost:8085/index.html`**
