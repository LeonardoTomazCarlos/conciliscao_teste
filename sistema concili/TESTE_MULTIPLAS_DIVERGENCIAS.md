# 🔬 TESTE AVANÇADO - MÚLTIPLAS DIVERGÊNCIAS

## 📊 Arquivos Criados

### 📄 `extrato_multiplas_divergencias.csv` (13 registros)
- Simula movimentações bancárias do período 01-05/10/2025
- Total: **R$ 7.723,00**

### 📝 `contabil_multiplas_divergencias.csv` (15 registros)  
- Simula lançamentos contábeis do mesmo período
- Total: **R$ 11.777,00**

## 🎯 Divergências Planejadas (6 total)

### 💰 Diferenças de Valores (2)
| Documento | Extrato | Contábil | Diferença | Tipo |
|-----------|---------|----------|-----------|------|
| **TED004** | R$ 2.200,00 | R$ 2.500,00 | R$ 300,00 | Valor maior no contábil |
| **BOL008** | R$ -180,00 | R$ 160,00 | R$ 20,00 | Diferença de valor + sinal |

### 📄 Registros Órfãos - Só no Extrato (1)
| Documento | Valor | Descrição |
|-----------|-------|-----------|
| **TRF009** | R$ 1.100,00 | Transferência Recebida |

### 📝 Registros Órfãos - Só no Contábil (3)
| Documento | Valor | Descrição |
|-----------|-------|-----------|
| **COM014** | R$ 420,00 | Comissão Vendas |
| **ALU015** | R$ 1.200,00 | Aluguel Escritório |
| **SER016** | R$ 500,00 | Serviços Contábeis |

## 📈 Estatísticas Esperadas

### ✅ Registros Conciliados: 10/12 (83,3%)
- PIX001, DEP002, PAG003, TAR005, PIX006, CHE007, SAQ010, PIX011, TAX012, DEP013

### ⚠️ Taxa de Divergência: 16,7%
- **Diferença Total**: R$ 4.054,00
- **Tipos de Problema**: Valores, Registros Órfãos

## 🧪 Cenários de Teste

### 1. **Detecção de Valores Diferentes**
- Sistema deve identificar TED004 e BOL008
- Mostrar valores lado a lado
- Calcular diferenças exatas

### 2. **Identificação de Órfãos**  
- Listar TRF009 (só extrato)
- Listar COM014, ALU015, SER016 (só contábil)
- Classificar corretamente cada tipo

### 3. **Relatório Estatístico**
- Taxa de conciliação ~83%
- Total de divergências: 6
- Diferença financeira: R$ 4.054,00

### 4. **Funcionalidades de Filtro**
- Filtrar por tipo de divergência
- Filtrar por período (01-05/10/2025)
- Buscar por documento específico

## 🚀 Como Executar

```bash
# 1. Análise prévia (opcional)
python analisar_multiplas_divergencias.py

# 2. Iniciar servidor (se não estiver rodando)
python app.py

# 3. Acessar aplicação
http://localhost:5000
```

## 🎯 Resultados Esperados

### ✅ O Sistema Deve Mostrar:
- **Dashboard** com estatísticas das 6 divergências
- **Lista detalhada** de cada inconsistência  
- **Filtros funcionais** por data e tipo
- **Relatório exportável** em CSV/Excel
- **Indicadores visuais** (gráficos, percentuais)

### ❌ Problemas a Investigar:
- Divergências não detectadas
- Classificação incorreta
- Cálculos de diferença errados
- Filtros que não funcionam
- Relatórios incompletos

---
📅 **Criado**: 02/10/2025  
🔬 **Complexidade**: Avançada  
✅ **Status**: Pronto para teste completo