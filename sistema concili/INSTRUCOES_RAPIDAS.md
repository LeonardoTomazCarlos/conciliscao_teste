# 🚀 Guia Rápido - Sistema de Conciliação Bancária

## ⚡ Início Rápido

### 1. Instalação
```bash
pip install -r requirements.txt
python app.py
```

### 2. Acesso
- URL: `http://localhost:5000`
- Usuário: `admin`
- Senha: `admin123`

## 📊 Fluxo de Trabalho

### 1. Importação de Dados
1. **Dashboard** → Upload rápido de arquivos
2. **Importação** → Upload detalhado com validação
3. Formatos suportados: CSV, Excel, OFX, CNAB, PDF

### 2. Conciliação Automática
1. **Relatórios** → "Conciliação Automática"
2. Sistema executa:
   - Detecção de transações recorrentes
   - Aplicação de regras configuradas
   - Verificação de divergências

### 3. Conciliação Manual
1. **Conciliação** → Selecione extrato e lançamento
2. Confirme a conciliação
3. Adicione observações se necessário

### 4. Gestão de Divergências
1. **Divergências** → Visualize alertas
2. Resolva cada divergência com justificativa
3. Acompanhe histórico de resoluções

## ⚙️ Configurações Essenciais

### 1. Contas Bancárias
- **Configurações** → "Contas Bancárias"
- Adicione suas contas para melhor organização

### 2. Regras de Conciliação
- **Configurações** → "Regras de Conciliação"
- Crie regras para automatizar a conciliação:
  - **Por Valor:** Transações com valores específicos
  - **Por Descrição:** Palavras-chave na descrição
  - **Por Documento:** Número de documento
  - **Recorrentes:** Padrões de transações

### 3. Usuários e Perfis
- **Configurações** → "Gestão de Usuários"
- Perfis disponíveis:
  - **Admin:** Acesso total
  - **Usuário:** Operações básicas
  - **Auditor:** Apenas visualização

## 🔍 Dicas de Uso

### Importação Eficiente
- Use arquivos CSV para melhor compatibilidade
- Mantenha colunas: Data, Descrição, Valor, Tipo
- O sistema detecta automaticamente as colunas

### Conciliação Inteligente
- Configure regras antes de importar dados
- Use conciliação automática primeiro
- Revise divergências antes de resolver

### Relatórios Úteis
- **Dashboard:** Visão geral em tempo real
- **Relatórios:** Análises detalhadas por período
- **Auditoria:** Histórico completo de ações

## 🚨 Solução de Problemas

### Erro de Upload
- Verifique formato do arquivo
- Confirme tamanho (máx. 16MB)
- Valide estrutura das colunas

### Conciliação Não Funciona
- Verifique se há dados importados
- Configure regras de conciliação
- Revise divergências pendentes

### Problemas de Login
- Use credenciais padrão: admin/admin123
- Verifique se o servidor está rodando
- Limpe cache do navegador

## 📈 Melhores Práticas

### Organização
1. Configure contas bancárias primeiro
2. Crie regras de conciliação
3. Importe dados em lotes pequenos
4. Revise divergências regularmente

### Segurança
1. Altere senha padrão do admin
2. Configure usuários com perfis adequados
3. Monitore logs de auditoria
4. Faça backup regular dos dados

### Performance
1. Processe arquivos grandes em horários de baixo uso
2. Configure regras eficientes
3. Limpe dados antigos periodicamente
4. Monitore uso de recursos

## 🔗 APIs Disponíveis

### Endpoints Principais
- `GET /api/extratos` - Listar extratos
- `GET /api/lancamentos` - Listar lançamentos
- `POST /api/conciliar` - Realizar conciliação
- `GET /api/estatisticas` - Estatísticas gerais
- `POST /api/conciliacao-automatica` - Conciliação automática

### Autenticação
- Todas as APIs requerem login
- Use sessão do navegador para autenticação
- Para integração externa, implemente autenticação por token

## 📞 Suporte

### Logs Importantes
- `logs/conciliacao.log` - Logs gerais do sistema
- Banco de dados: `instance/conciliacao.db`

### Comandos Úteis
```bash
# Verificar dependências
pip list

# Limpar cache
rm -rf __pycache__

# Backup do banco
cp instance/conciliacao.db backup_$(date +%Y%m%d).db
```

### Recursos Adicionais
- Documentação completa: `README.md`
- Exemplos de arquivos: `exemplos/`
- Templates: `templates/`

---

**💡 Dica:** Comece com dados de teste para familiarizar-se com o sistema antes de usar dados reais. 