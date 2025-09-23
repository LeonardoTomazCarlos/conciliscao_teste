# 📋 GUIA DE TESTE DE DIVERGÊNCIAS

## 🎯 **ARQUIVOS CRIADOS PARA TESTE**

### **1. Arquivos Principais:**
- **`extrato_bancario_teste_divergencias.csv`** - Extrato bancário com divergências
- **`lancamentos_contabeis_teste_divergencias.csv`** - Lançamentos contábeis com divergências

### **2. Arquivos Complexos Adicionais:**
- **`extrato_bancario_divergencias_complexas.csv`** - Casos mais complexos
- **`lancamentos_contabeis_divergencias_complexas.csv`** - Casos mais complexos

---

## 🔍 **TIPOS DE DIVERGÊNCIAS INCLUÍDAS**

### **📊 RESUMO QUANTITATIVO (Arquivos Principais):**
- **Órfãos no extrato:** 2 registros
- **Órfãos nos lançamentos:** 3 registros  
- **Divergências de valor:** 1 caso
- **Duplicatas no extrato:** 2 registros
- **🎯 TOTAL:** 8 divergências

### **🔍 DETALHES DAS DIVERGÊNCIAS:**

#### **1️⃣ Órfãos no Extrato (sem correspondência contábil):**
- **Data:** 2025-09-23 - **Descrição:** "DIVERGÊNCIA VALOR - Transferência errada" - **Valor:** R$ 999,99
- **Data:** 2025-09-24 - **Descrição:** "ÓRFÃO EXTRATO - Sem correspondência contábil" - **Valor:** R$ 777,77

#### **2️⃣ Órfãos nos Lançamentos (sem correspondência no extrato):**
- **Data:** 2025-09-23 - **Descrição:** "VALOR DIFERENTE - Transferência registrada errado" - **Valor:** R$ 1.500,00
- **Data:** 2025-09-26 - **Descrição:** "ÓRFÃO CONTÁBIL - Lançamento sem extrato" - **Valor:** R$ 333,33
- **Data:** 2025-09-26 - **Descrição:** "DATA DIVERGENTE - Lançamento data errada" - **Valor:** R$ 600,00

#### **3️⃣ Divergências de Valor:**
- **Data:** 2025-09-23 - **Diferença:** R$ 500,01 entre extrato (R$ 999,99) e lançamento (R$ 1.500,00)

#### **4️⃣ Duplicatas no Extrato:**
- **Data:** 2025-09-25 - **Descrição:** "DUPLICATA - Mesmo pagamento duas vezes" - **Valor:** R$ 250,00 (2x)

---

## 🚀 **COMO TESTAR NO SISTEMA**

### **📋 Passo a Passo:**

1. **Acesse o sistema:**
   ```
   http://localhost:5000
   ```

2. **Faça login** (se necessário)

3. **Navegue para a aba "Upload de Dados"**

4. **Faça upload dos arquivos:**
   - **Extrato Bancário:** `extrato_bancario_teste_divergencias.csv`
   - **Lançamentos Contábeis:** `lancamentos_contabeis_teste_divergencias.csv`

5. **Execute a conciliação:**
   - Clique em "Executar Conciliação"
   - Aguarde o processamento

6. **Verifique as divergências:**
   - Navegue para a aba "Divergências"
   - Deve exibir **8 divergências** detectadas

---

## 🔧 **ARQUIVOS COMPLEXOS ADICIONAIS**

### **📁 Para Testes Avançados:**
- **`extrato_bancario_divergencias_complexas.csv`**
- **`lancamentos_contabeis_divergencias_complexas.csv`**

#### **🎯 Casos Especiais Incluídos:**
- **Valores aproximados** (diferença de centavos)
- **Datas divergentes** (mesmo valor, data diferente)
- **Valores parciais** (estornos, descontos)
- **Transações internacionais** (diferenças de câmbio)
- **Taxas bancárias** não previstas
- **Juros sobre aplicações**

---

## ✅ **VALIDAÇÃO ESPERADA**

### **🎯 Resultados que o Sistema Deve Detectar:**

1. **Divergências por Órfãos:**
   - 2 registros do extrato sem correspondência
   - 3 registros de lançamentos sem correspondência

2. **Divergências por Valor:**
   - 1 caso de valores diferentes para a mesma transação

3. **Duplicatas:**
   - 2 registros duplicados no extrato

4. **Status das Conciliações:**
   - Transações que coincidem devem aparecer como "Conciliado"
   - Divergências devem aparecer como "Divergente"

---

## 🛠️ **SCRIPTS DE APOIO**

### **📄 Script de Análise:**
```bash
python processar_divergencias_teste.py
```
- Analisa os arquivos e exibe relatório detalhado
- Útil para debug e verificação prévia

### **🔍 Verificação Rápida:**
Abra os arquivos CSV em qualquer editor e procure por:
- **"DIVERGÊNCIA"**, **"ÓRFÃO"**, **"DUPLICATA"** nas descrições
- **Valores únicos** como R$ 999,99, R$ 777,77, R$ 333,33
- **Datas específicas** como 2025-09-23, 2025-09-24, 2025-09-26

---

## 🎉 **SUCESSO!**

Agora você tem arquivos completos para testar todas as funcionalidades de detecção de divergências do sistema de conciliação!

**📞 Suporte:** Se encontrar problemas, verifique os logs do sistema ou execute o script de análise para debug.