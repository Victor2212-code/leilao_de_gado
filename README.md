
# 🐂 Sistema de Leilão de Gado

Este é um sistema web completo de leilões online de gado desenvolvido com Django. Ele permite o cadastro de compradores, vendedores, entregadores e administradores, com funcionalidades como lances em tempo real, gerenciamento de animais, pagamentos e entregas.



## 🔧 Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Django 5.1.6](https://docs.djangoproject.com/en/5.1/)
- [SQLite](https://www.sqlite.org/index.html) (padrão)
- [Bootstrap 5](https://getbootstrap.com/)
- [JavaScript (Fetch API)](https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API)
- [Python Decouple](https://pypi.org/project/python-decouple/) (para variáveis de ambiente)



## 🗂️ Funcionalidades

### 👤 Usuários
- Cadastro e login de compradores, vendedores, administradores e entregadores
- Perfis com dados detalhados

### 🐮 Animais
- Cadastro de animais com imagem, raça, idade, peso, valor mínimo e data de leilão
- Página de listagem e pesquisa com contagem regressiva para término

### 💸 Lances
- Compradores podem dar lances em tempo real
- Bloqueio automático após o término do leilão
- Histórico de lances e vencedores

### 💬 Chat
- Sistema de mensagens entre compradores e vendedores

### 📦 Entregas
- Compradores escolhem o entregador
- Entregadores podem aceitar e confirmar entregas

### 💳 Pagamentos
- Suporte a PIX (com QR Code), boleto e cartão
- Confirmação de pagamento com notificação para o vendedor

### 📊 Administração
- Painel de administrador para gerenciar usuários, entregadores e mensagens
- Dashboard com relatórios financeiros e estatísticas



## 📁 Estrutura do Projeto

```

leilao\_gado/
│
├── animais/          # App de gestão dos animais e leilões
├── chat/             # App de mensagens entre usuários
├── entregador/       # App de entregadores
├── pagamentos/       # App de pagamentos
├── usuarios/         # App de autenticação e perfis
├── administrador/    # App para o painel administrativo
│
├── templates/        # Templates HTML
├── staticfiles/      # Arquivos estáticos coletados
├── media/            # Imagens de animais e uploads
├── .env              # Variáveis de ambiente (não versionar!)
└── manage.py



````
## ▶️ Como Rodar Localmente

### 1. Clone o projeto
```bash
git clone https://github.com/seuusuario/leilao_gado.git
cd leilao_gado
````

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Crie o arquivo `.env`

```bash
touch .env
```

Preencha com:

```env
SECRET_KEY_DJANGO=coloque_sua_chave_secreta_aqui
```

### 5. Aplique as migrações e crie um superusuário

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)



## 🛡️ Segurança e Boas Práticas

* Uso de variáveis sensíveis via `.env`
* Interface responsiva e segura
* Proteção com CSRF e autenticação com sessão
* Separação de permissões por tipo de usuário



## 📌 Próximos Passos

* Implementar testes automatizados
* Integração com gateways de pagamento reais
* Deploy na nuvem (Heroku, Render ou Railway)
* Integração com WebSockets para chat e lances em tempo real



## 📄 Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).


## 👨‍💻 Autor

Desenvolvido por Victor Hugo Assumpção de Amorim – [LinkedIn](https://www.linkedin.com/in/devvictorhugo) | [GitHub](https://github.com/Victor2212-code)

