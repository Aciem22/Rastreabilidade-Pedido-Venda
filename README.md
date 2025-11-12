# 🚚 Sistema de Rastreabilidade de Remessas – Omie x Streamlit

Aplicação em **Python + Streamlit** integrada à **API do ERP Omie**, desenvolvida para gerenciar e atualizar informações de **lotes e validades** de produtos em **remessas**.  
O sistema permite consultar clientes, listar remessas, editar dados de rastreabilidade e enviar alterações diretamente para o ERP.

---

## 🧠 Funcionalidades

- 🔍 Consulta automática de **clientes** via CNPJ/CPF  
- 📋 Listagem das **remessas** associadas ao cliente  
- 📦 Edição dos campos de **lote**, **fabricação** e **validade** dos produtos  
- 🔄 Envio das alterações para a **API Omie** (`AlterarRemessa`)  
- 🧾 Registro automático de volumes (`frete.nQtdVol`)  
- ⚙️ Cache inteligente com `st.cache_data` para evitar chamadas repetidas  
- 💻 Interface limpa e responsiva com **Streamlit**  
- 🔗 Acesso rápido ao módulo de **Rastreabilidade de Pedidos de Venda**

---

🧩 Tecnologias Usadas

🐍 Python 3.11+ - Linguagem principal

🎈 Streamlit - Interface web

🌐 Requests - Comunicação com API Omie

🧠 Pandas - Manipulação de dados

💾 JSON - Estrutura das requisições
