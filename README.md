📞 Controle de Telefonia

Um sistema desktop feito em Python com Tkinter, desenvolvido para gerenciar linhas telefônicas corporativas.
O programa permite cadastrar, consultar, atualizar, inativar e exportar informações de linhas telefônicas de forma prática e segura, com integração a um banco de dados SQLite e exportação para Excel (.xlsx) via OpenPyXL.

💡 Funcionalidades

✅ Cadastro de Linhas Telefônicas

Armazena número, responsável, operadora, valor e centro de custo.

Valida número (deve conter 11 dígitos).

Impede duplicidade de cadastro.

🔍 Consulta de Linhas

Busca por número ou responsável.

Exibe resultados ativos e oferece opção para visualizar linhas inativas.

🔄 Atualização de Dados

Permite editar registros existentes, com confirmação antes de salvar as alterações.

❌ Inativação (Exclusão Lógica)

Inativa registros sem apagá-los do banco (mantém histórico).

📤 Exportação Personalizada

Gera planilha Excel com filtros por operadora (Vivo, Claro, Tim) e status (ativas/inativas/todas).

Exporta automaticamente para:

C:\ProgramData\ControleTelefonia\Exportacoes


💾 Banco de Dados Local (SQLite)

O banco é criado em:

C:\ProgramData\ControleTelefonia\banco_telefonia.db

🖥️ Interface
  <img width="792" height="519" alt="Captura de tela 2025-11-04 153642" src="https://github.com/user-attachments/assets/d48e536d-52be-4dc7-b9d6-c426e1951e69" />
  <img width="420" height="298" alt="Captura de tela 2025-11-04 153802" src="https://github.com/user-attachments/assets/5c176a82-a526-42c1-9107-49fac91d76af" />


🎨 Cores e estilo:
Fundo amarelo-claro #f6fa84 e botões destacados para boa legibilidade.

🗂️ Estrutura do Projeto
ControleTelefonia/
│
├── controle_telefonia.py      # Código principal (interface + lógica)
├── banco_telefonia.db         # Banco de dados (criado automaticamente)
└── Exportacoes/               # Pasta de planilhas geradas (criada automaticamente)

⚙️ Tecnologias Utilizadas

Python 3.10+

Tkinter → Interface gráfica

SQLite3 → Banco de dados local

OpenPyXL → Geração de planilhas Excel

Datetime / OS → Manipulação de datas e diretórios

🚀 Como Executar

Instale as dependências (se necessário):

pip install openpyxl


Baixe ou clone o repositório:

git clone https://github.com/seuusuario/ControleTelefonia.git


Execute o programa:

python controle_telefonia.py


Pronto! O sistema abrirá em uma janela gráfica.

📋 Exemplo de Uso

Preencha todos os campos e clique em 💾 Salvar.

Consulte pelo número ou nome em 🔍 Consultar.

Selecione uma linha e clique em 🔄 Atualizar para editar.

Clique em ❌ Excluir para inativar uma linha.

Use 📤 Exportar para gerar uma planilha com filtros.

🧠 Boas Práticas e Dicas

Sempre feche o programa corretamente para evitar bloqueio no banco SQLite.

Prefira números de telefone sem formatação (apenas dígitos).

Use valores decimais com ponto (.), exemplo: 49.99.

Para evitar erros, mantenha permissões de escrita na pasta C:\ProgramData.

👨‍💻 Autor

Desenvolvido por: Evelin Silva

