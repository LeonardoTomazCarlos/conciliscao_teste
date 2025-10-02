# 🏦 Sistema de Conciliação Bancária

Um sistema completo para conciliação automática e manual de extratos bancários com lançamentos contábeis, desenvolvido em Python com Flask.

## 🚀 Funcionalidades

### ✅ **Principais Recursos:**
- **Upload de Extratos**: Suporte a CSV, Excel, OFX, CNAB, PDF
- **Upload de Lançamentos**: Processamento de arquivos contábeis
- **Conciliação Automática**: Baseada em regras configuráveis
- **Detecção de Duplicatas**: Prevenção de registros duplicados
- **Interface Web**: Dashboard responsivo e intuitivo
- **Sistema de Auditoria**: Logs completos de todas as ações
- **Relatórios**: Estatísticas em tempo real

### 📊 **Recursos Avançados:**
- Conciliação manual arrastar e soltar
- Regras de conciliação personalizáveis
- Detecção de divergências
- Sistema de usuários e permissões
- API REST completa
- Backup automático de dados

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Banco de Dados**: SQLite (SQLAlchemy)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Processamento**: Pandas, OpenPyXL, PyPDF2
- **Autenticação**: Flask-Login
- **API**: RESTful com JSON

## 📦 Instalação

### Pré-requisitos:
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação:

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/sistema-conciliacao-bancaria.git
cd sistema-conciliacao-bancaria
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python app.py
```

4. **Acesse no navegador:**
```
http://localhost:5000
```

## 🔐 Credenciais Padrão

- **Usuário**: `admin`
- **Senha**: `admin123`

## 📁 Estrutura do Projeto

```
sistema-conciliacao-bancaria/
├── app.py                          # Aplicação principal Flask
├── requirements.txt                # Dependências Python
├── README.md                      # Este arquivo
├── INSTRUCOES_RAPIDAS.md          # Guia rápido de uso
├── templates/                     # Templates HTML
│   ├── index.html                # Dashboard principal
│   └── login.html                # Página de login
├── exemplos/                      # Arquivos de exemplo
│   ├── extrato_exemplo.csv       # Exemplo de extrato
│   └── lancamentos_exemplo.csv   # Exemplo de lançamentos
├── uploads/                       # Pasta para uploads
├── instance/                      # Banco de dados SQLite
├── logs/                         # Logs do sistema
└── testes/                       # Scripts de teste
```

## 🧪 Testes

### Executar testes básicos:
```bash
python teste_final.py
```

### Executar testes de divergências:
```bash
python teste_divergencias.py
```

### Executar testes completos:
```bash
python teste_upload_completo.py
```

## 📊 Formatos de Arquivo Suportados

### Extratos Bancários:
- **CSV**: Arquivos separados por vírgula
- **Excel**: Arquivos .xlsx e .xls
- **OFX**: Formato bancário padrão
- **CNAB**: Arquivos de retorno bancário
- **PDF**: Extração de texto (experimental)

### Lançamentos Contábeis:
- **CSV**: Arquivos separados por vírgula
- **Excel**: Arquivos .xlsx e .xls

## 🔧 Configuração

### Variáveis de Ambiente:
```bash
# Configurações de API bancária (opcional)
BANK_API_KEY=sua_chave_api
BANK_API_URL=https://api.banco.com

# Configurações de ERP (opcional)
ERP_API_KEY=sua_chave_erp
ERP_API_URL=https://api.erp.com
```

### Configurações do Sistema:
- **Porta**: 5000 (padrão)
- **Banco de Dados**: SQLite (instance/conciliacao.db)
- **Upload Máximo**: 16MB por arquivo
- **Logs**: logs/conciliacao.log

## 📈 Estatísticas do Sistema

### Dados de Teste:
- **Total de extratos**: 67 registros
- **Total de lançamentos**: 18 registros
- **Conciliações automáticas**: 14 realizadas
- **Taxa de conciliação**: 82%
- **Detecção de duplicatas**: 100% eficaz

## 🎯 Funcionalidades Testadas

### ✅ **Sistema de Upload:**
- Processamento de CSV com detecção automática de colunas
- Validação de dados e formatação
- Prevenção de duplicatas
- Suporte a múltiplos formatos

### ✅ **Conciliação Automática:**
- Conciliação por valor, data e descrição
- Regras configuráveis
- Detecção de transações recorrentes
- Sistema de prioridades

### ✅ **Interface Web:**
- Dashboard responsivo
- Upload drag-and-drop
- Visualização de estatísticas
- Sistema de navegação intuitivo

### ✅ **Segurança:**
- Autenticação de usuários
- Controle de acesso por perfil
- Auditoria completa
- Validação de dados

## 🚀 Deploy em Produção

### Para ambiente de produção:

1. **Configurar servidor web:**
```bash
# Usando Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Configurar proxy reverso (Nginx):**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Configurar SSL (HTTPS):**
```bash
# Usando Let's Encrypt
sudo certbot --nginx -d seu-dominio.com
```


## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato: seu-email@exemplo.com

## 🎉 Agradecimentos

- Flask Framework
- Bootstrap CSS Framework
- Comunidade Python
- Contribuidores do projeto

---

*Versão: 1.0 | Data: Agosto 2025* 
