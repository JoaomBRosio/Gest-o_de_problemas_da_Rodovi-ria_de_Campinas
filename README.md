# Sistema de Relato e Gerenciamento de Problemas na Rodoviária 🚌

![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)
![gTTS](https://img.shields.io/badge/gTTS-2.2.3-brightgreen)
![Pygame](https://img.shields.io/badge/Pygame-2.0.1-lightgrey)
![psycopg2](https://img.shields.io/badge/psycopg2-2.9.5-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.3-blue)

Este projeto consiste em um sistema para gestão de problemas reportados na rodoviária, com um chat exclusivo para funcionários. Usuários podem relatar problemas adicionando título, descrição e imagem. Funcionários têm a possibilidade de visualizar, buscar e resolver problemas, além de poder tocar alertas de áudio para notificar sobre problemas críticos em setores específicos.

## Índice
- [Funcionalidades](#funcionalidades)
- [Configuração](#configuração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)

---

### Funcionalidades
- **Cadastro e Login de Usuários**: Cada usuário pode se cadastrar e fazer login, com acesso diferenciado para usuários do tipo `admin` e `funcionário`.
- **Cadastro de Problemas**: Permite que qualquer usuário registre problemas com título, descrição e imagem.
- **Chat para Funcionários**: Funcionários têm acesso a um chat onde podem visualizar e gerenciar problemas relatados.
- **Setores**: Adição e exclusão de setores para organização e relatórios mais específicos.
- **Alertas de Áudio**: Utiliza a biblioteca `gTTS` para gerar e `pygame` para tocar alertas de áudio que notificam sobre problemas verificados em setores específicos.
- **Busca e Resolução de Problemas**: Possibilidade de busca de problemas pelo título, além de marcar problemas como resolvidos.

---

### Configuração

#### 1. Pré-requisitos
- Python 3.7 ou superior
- PostgreSQL (para banco de dados, eu usei o PgAdmin)
  
#### 2. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


3. Instalar as Dependências
bash
Copiar código
pip install -r requirements.txt

4. Configuração do Banco de Dados
Crie o banco de dados e configure as variáveis DB_HOST, DB_NAME, DB_USER, e DB_PASSWORD no código para conectar ao seu banco PostgreSQL.

5. Executar o Projeto
bash
Copiar código
python app.py

Tecnologias Utilizadas
Flask: Framework para criação da aplicação web.
psycopg2: Biblioteca para conexão com o banco de dados PostgreSQL.
gTTS: Para geração de áudio a partir de texto.
Pygame: Para reprodução dos áudios gerados.

HTML/CSS: Para construção das interfaces das páginas.

Estrutura do Projeto
plaintext

├── app.py               # Arquivo principal da aplicação
├── templates/           # Diretório com os arquivos HTML
|   ├── cadastro.html
|   ├── login.html
|   ├── home.html
|   ├── chat.html
|   ├── relatar_problema.html
├── static/              # Arquivos estáticos (CSS, JS, etc)
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo README


Como Usar

Acesse a página de cadastro e registre-se com suas informações.
Após o login, você pode relatar problemas na página dedicada.
Funcionários e administradores podem acessar o chat para visualizar e gerenciar os problemas relatados.
Na página de verificação, é possível gerar alertas de áudio para notificar sobre problemas críticos.
