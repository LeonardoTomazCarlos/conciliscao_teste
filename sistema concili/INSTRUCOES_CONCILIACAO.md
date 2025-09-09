# 📋 Instruções para Conciliação Bancária

## 📁 Arquivos Gerados

Foram criados 4 arquivos CSV para você testar o sistema de conciliação:

### 1. **extrato_bancario_exemplo.csv**
- **Conteúdo**: 20 transações bancárias de setembro/2024
- **Período**: 01/09 a 10/09/2024
- **Valores**: R$ 25,30 a R$ 5.000,00
- **Tipos**: Créditos e débitos
- **Uso**: Upload como extrato bancário

### 2. **lancamentos_contabeis_exemplo.csv**
- **Conteúdo**: 20 lançamentos contábeis correspondentes
- **Período**: 01/09 a 10/09/2024
- **Categorias**: Receitas, Alimentação, Transporte, Saúde, etc.
- **Uso**: Upload como lançamentos contábeis

### 3. **extrato_bancario_divergencias.csv**
- **Conteúdo**: 20 transações com pequenas divergências
- **Período**: 11/09 a 20/09/2024
- **Divergência**: Valor do combustível (R$ 125,00 vs R$ 120,00)
- **Uso**: Testar detecção de divergências

### 4. **lancamentos_contabeis_divergencias.csv**
- **Conteúdo**: 20 lançamentos com divergência
- **Período**: 11/09 a 20/09/2024
- **Divergência**: Valor do combustível (R$ 120,00 vs R$ 125,00)
- **Uso**: Testar resolução de divergências

## 🚀 Como Usar

### Passo 1: Upload dos Arquivos
1. Acesse o sistema em `http://localhost:8080`
2. Faça login com suas credenciais
3. Vá para a aba **"Upload"**
4. Faça upload do arquivo `extrato_bancario_exemplo.csv`
5. Faça upload do arquivo `lancamentos_contabeis_exemplo.csv`

### Passo 2: Conciliação Automática
1. Vá para a aba **"Conciliação"**
2. Clique em **"Executar Conciliação Automática"**
3. O sistema irá conciliar automaticamente as transações que coincidem

### Passo 3: Conciliação Manual
1. Na aba **"Conciliação"**, visualize as transações não conciliadas
2. Selecione um extrato e um lançamento correspondente
3. Clique em **"Conciliar"** para fazer a conciliação manual

### Passo 4: Testar Divergências
1. Faça upload dos arquivos com divergências:
   - `extrato_bancario_divergencias.csv`
   - `lancamentos_contabeis_divergencias.csv`
2. Execute a conciliação automática
3. O sistema detectará a divergência no valor do combustível
4. Resolva a divergência manualmente

## 📊 Dados dos Arquivos

### Transações Incluídas:
- **Transferências PIX**: João Silva, Maria Santos, Pedro Costa, etc.
- **Compras com cartão**: Supermercado, Posto, Farmácia, Restaurante
- **Depósitos**: Dinheiro e cheques
- **Saques**: ATM
- **Salário**: Empresa XYZ

### Valores Totais:
- **Extrato**: R$ 13.196,10 (créditos) - R$ 1.286,10 (débitos) = R$ 11.910,00
- **Lançamentos**: R$ 13.196,10 (créditos) - R$ 1.281,10 (débitos) = R$ 11.915,00

## 🔍 Divergências para Testar

### Arquivo de Divergências:
- **Data**: 13/09/2024
- **Descrição**: Combustível Posto Gasolina
- **Extrato**: R$ 125,00
- **Lançamento**: R$ 120,00
- **Diferença**: R$ 5,00

## 📈 Funcionalidades para Testar

1. **Upload de Arquivos**: CSV com diferentes formatos
2. **Conciliação Automática**: Por valor, data e tipo
3. **Conciliação Manual**: Seleção de registros
4. **Detecção de Divergências**: Valores diferentes
5. **Relatórios**: Estatísticas e exportação
6. **Filtros**: Por período, categoria, status
7. **Auditoria**: Log de todas as operações

## 🎯 Objetivos dos Testes

- ✅ Verificar upload e processamento de arquivos
- ✅ Testar conciliação automática e manual
- ✅ Validar detecção de divergências
- ✅ Confirmar geração de relatórios
- ✅ Testar filtros e busca
- ✅ Verificar logs de auditoria

## 📝 Próximos Passos

1. Execute os uploads conforme instruções
2. Teste todas as funcionalidades
3. Verifique os relatórios gerados
4. Confirme o funcionamento dos filtros
5. Valide a auditoria do sistema

---

**💡 Dica**: Use os arquivos em sequência para uma experiência completa de teste do sistema de conciliação bancária!
