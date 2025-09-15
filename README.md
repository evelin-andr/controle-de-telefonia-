📱 Controle de Telefonia

Um aplicativo simples em Python + Tkinter para gerenciar linhas de telefonia.

✨ Funcionalidades

✔️ Cadastro de linhas com:

Número de telefone (11 dígitos, formatado automaticamente)

Responsável / Usuário

Operadora (Vivo, Claro, Tim)

Valor da linha (formatado em R$)

Centro de custo (em maiúsculo)

✔️ Validação dos campos antes de salvar.
✔️ Navegação entre campos com Enter ou setas ⬆️⬇️.
✔️ Tabela para exibir os dados cadastrados.
✔️ Limpeza automática dos campos após salvar.

⚠️ As funções Consultar e Atualizar ainda estão em desenvolvimento.

🛠️ Tecnologias utilizadas

Python 3.x

Tkinter
 (biblioteca padrão do Python)

ttk (para widgets mais modernos, como o Combobox)

🚀 Como executar

Clone este repositório:

git clone <URL_DO_REPOSITORIO>


Acesse a pasta:

cd controle-telefonia


Execute o programa:

python main.py

📂 Estrutura do projeto
controle-telefonia/
│
├── main.py           
├── README.md       
└── requirements.txt 

📦 Dependências

Criei um arquivo requirements.txt para manter o padrão de projetos Python.
Mesmo o Tkinter já vindo junto com o Python, deixei registrado:

tk

Instalação (opcional):

pip install -r requirements.txt

🎯 Próximos passos

Implementar função Consultar para buscar linhas já cadastradas.

Implementar função Atualizar para editar registros existentes.
