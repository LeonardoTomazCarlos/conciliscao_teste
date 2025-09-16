# 🧪 GUIA COMPLETO DE TESTES - SISTEMA DE CONCILIAÇÃO

## 📋 Arquivos Criados para Teste

### 1. 📊 **Cenário Básico - Conciliações Normais**
- `extrato_teste_dezembro.csv` - 29 transações de extrato
- `lancamentos_teste_dezembro.csv` - 31 lançamentos contábeis
- **Teste**: Conciliações automáticas com algumas divergências propositais

### 2. 🔄 **Cenário de Duplicatas**
- `extrato_com_duplicatas.csv` - Contém transações duplicadas
- `lancamentos_com_duplicatas.csv` - Contém lançamentos duplicados
- **Teste**: Detecção automática de duplicatas

### 3. 💰 **Cenário de Diferenças de Valor**
- `extrato_diferenca_valores.csv` - Valores ligeiramente diferentes
- `lancamentos_diferenca_valores.csv` - Valores com pequenas diferenças
- **Teste**: Detecção de divergências de valor entre extrato e lançamento

### 4. 🔍 **Cenário de Órfãos**
- `extratos_orfaos.csv` - Extratos sem lançamentos correspondentes
- `lancamentos_orfaos.csv` - Lançamentos sem extratos correspondentes
- **Teste**: Detecção de transações órfãs

### 5. 📅 **Cenário de Datas Divergentes**
- `extrato_datas_divergentes.csv` - Transações com datas específicas
- `lancamentos_datas_divergentes.csv` - Mesmos valores mas datas diferentes
- **Teste**: Detecção de divergências de data

## 🚀 PASSO A PASSO PARA TESTAR

### **ETAPA 1: Preparar o Sistema**
1. Acesse: `http://localhost:5000`
2. Faça login no sistema
3. Vá para a aba "Conciliação"

### **ETAPA 2: Limpar Dados Anteriores (Opcional)**
1. Execute: `python limpar_dados.py` no terminal
2. Isso remove dados anteriores para teste limpo

### **ETAPA 3: Testar Cenário Básico**
1. **Upload Extrato**: `extrato_teste_dezembro.csv`
2. **Upload Lançamentos**: `lancamentos_teste_dezembro.csv`
3. **Executar Conciliação Automática**
4. **Verificar**:
   - Conciliações realizadas
   - Divergências detectadas automaticamente
   - Filtros funcionando

### **ETAPA 4: Testar Duplicatas**
1. **Upload**: `extrato_com_duplicatas.csv` e `lancamentos_com_duplicatas.csv`
2. **Verificar na aba Divergências**:
   - Tipo: "Duplicata"
   - Deve detectar as transações repetidas

### **ETAPA 5: Testar Diferenças de Valor**
1. **Upload**: `extrato_diferenca_valores.csv` e `lancamentos_diferenca_valores.csv`
2. **Executar Conciliação**
3. **Verificar Divergências**:
   - Tipo: "Diferença de Valor"
   - Valores como R$ 1200 vs R$ 1205

### **ETAPA 6: Testar Órfãos**
1. **Upload**: `extratos_orfaos.csv` e `lancamentos_orfaos.csv`
2. **Verificar Divergências**:
   - Tipo: "Extrato Órfão"
   - Tipo: "Lançamento Órfão"

### **ETAPA 7: Testar Datas Divergentes**
1. **Upload**: `extrato_datas_divergentes.csv` e `lancamentos_datas_divergentes.csv`
2. **Verificar Divergências**:
   - Tipo: "Data Divergente"
   - Mesmo valor, datas diferentes

## 🎯 FUNCIONALIDADES PARA TESTAR

### **Na Aba Conciliação:**
- ✅ Upload de arquivos CSV
- ✅ Visualização de extratos e lançamentos
- ✅ Conciliação automática
- ✅ Conciliação manual
- ✅ Filtros por data, valor, status
- ✅ Estatísticas em tempo real

### **Na Aba Divergências:**
- ✅ Listagem de todas as divergências
- ✅ Filtros por tipo de divergência
- ✅ Filtros por status (pendente, resolvido)
- ✅ Filtros por data
- ✅ Resolução de divergências
- ✅ Estatísticas de divergências

### **Página de Teste Especial:**
- ✅ Acesse: `http://localhost:5000/teste_filtros_divergencias.html`
- ✅ Botão "Criar Divergências Teste"
- ✅ Teste todos os filtros
- ✅ Log de ações em tempo real

## 🐞 CENÁRIOS DE TESTE ESPECÍFICOS

### **Teste 1: Workflow Completo**
```
1. Upload extrato_teste_dezembro.csv
2. Upload lancamentos_teste_dezembro.csv  
3. Executar conciliação automática
4. Verificar divergências geradas
5. Aplicar filtros na aba divergências
6. Resolver algumas divergências
```

### **Teste 2: Detecção de Duplicatas**
```
1. Upload extrato_com_duplicatas.csv
2. Verificar detecção automática de 3 PIX duplicados
3. Upload lancamentos_com_duplicatas.csv
4. Verificar detecção de 2 lançamentos duplicados
```

### **Teste 3: Diferenças de Valor**
```
1. Upload extrato_diferenca_valores.csv + lancamentos_diferenca_valores.csv
2. Executar conciliação
3. Verificar divergências de valor:
   - R$ 1200 vs R$ 1205 (diferença R$ 5)
   - R$ 750.50 vs R$ 750.00 (diferença R$ 0.50)
   - R$ 2000 vs R$ 1995 (diferença R$ 5)
```

### **Teste 4: Filtros Avançados**
```
1. Filtrar por tipo: "Extrato Órfão"
2. Filtrar por data: Janeiro 2025
3. Filtrar por status: "Pendente"
4. Combinar filtros múltiplos
```

## 📊 RESULTADOS ESPERADOS

### **Métricas Típicas Após Testes:**
- **Conciliações**: ~60-70% das transações
- **Divergências**: ~30-40% dos dados
- **Tipos Detectados**:
  - Extrato Órfão: ~10-15 itens
  - Lançamento Órfão: ~8-10 itens  
  - Diferença Valor: ~5-8 itens
  - Duplicatas: ~3-5 itens
  - Data Divergente: ~3-5 itens

### **Performance Esperada:**
- Upload: < 2 segundos
- Conciliação: < 5 segundos
- Detecção divergências: < 3 segundos
- Filtros: < 1 segundo

## 🛠️ COMANDOS ÚTEIS PARA TESTE

### **Terminal/Prompt:**
```bash
# Executar detecção forçada de divergências
python forcar_deteccao_divergencias.py

# Análise completa do banco
python teste_divergencias_completo.py

# Limpar dados para novo teste
python limpar_dados.py

# Iniciar servidor
python app.py
```

### **URLs de Teste:**
- Sistema principal: `http://localhost:5000`
- Teste divergências: `http://localhost:5000/teste_filtros_divergencias.html`
- API divergências: `http://localhost:5000/api/divergencias`

## 🎯 CHECKLIST DE VALIDAÇÃO

### ✅ **Funcionalidades Básicas:**
- [ ] Upload de extratos
- [ ] Upload de lançamentos
- [ ] Conciliação automática
- [ ] Visualização de dados

### ✅ **Detecção de Divergências:**
- [ ] Extratos órfãos
- [ ] Lançamentos órfãos
- [ ] Duplicatas
- [ ] Diferenças de valor
- [ ] Datas divergentes

### ✅ **Interface e Filtros:**
- [ ] Filtros por tipo
- [ ] Filtros por status
- [ ] Filtros por data
- [ ] Estatísticas em tempo real
- [ ] Resolução de divergências

### ✅ **Performance e Estabilidade:**
- [ ] Upload de arquivos grandes
- [ ] Filtros responsivos
- [ ] Navegação entre abas
- [ ] Atualização automática

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### **Erro "Arquivo não encontrado"**
- Verifique se os arquivos CSV estão na pasta correta
- Confirme as permissões de arquivo

### **Divergências não aparecem**
- Execute: `python forcar_deteccao_divergencias.py`
- Verifique se a detecção automática está ativa

### **Filtros não funcionam**
- Recarregue a página
- Verifique se há dados para filtrar
- Teste com a página de teste especial

### **Performance lenta**
- Limpe dados antigos
- Reinicie o servidor
- Verifique logs de erro

---

## 🎉 CONCLUSÃO

Com estes arquivos, você pode testar **TODAS** as funcionalidades do sistema:

1. **Upload e processamento** de arquivos CSV
2. **Conciliação automática** inteligente  
3. **Detecção completa** de divergências
4. **Filtros avançados** e busca
5. **Interface responsiva** e amigável
6. **Resolução** de divergências
7. **Estatísticas** em tempo real

**Bom teste! 🚀**