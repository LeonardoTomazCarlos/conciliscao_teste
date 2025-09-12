# Arquivos de Exemplo para Conciliação

Este diretório contém arquivos de exemplo para testar o sistema de conciliação bancária.

## Arquivos Disponíveis

### 1. extrato_conciliacao_e_divergencias.csv
**Extrato bancário com 30 registros**
- Contém registros que irão conciliar perfeitamente
- Contém registros com divergências propositais 
- Todos os registros são da data 11/09/2025

### 2. lancamentos_conciliacao_e_divergencias.csv  
**Lançamentos contábeis com 31 registros**
- Contém lançamentos que correspondem aos extratos
- Contém lançamentos com valores ligeiramente diferentes (divergências)
- Contém 1 lançamento órfão (sem correspondência no extrato)
- Todos os registros são da data 11/09/2025

## Tipos de Divergências Incluídas

1. **Valores Diferentes**: Mesmo documento, valores distintos
2. **Registros Duplicados**: Extratos duplicados vs lançamento único
3. **Lançamentos Órfãos**: Lançamentos sem correspondência bancária
4. **Valores com Diferenças Pequenas**: Para testar tolerância do sistema

## Como Usar

1. **Importe o extrato**: Use a funcionalidade de importação do sistema para carregar `extrato_conciliacao_e_divergencias.csv`
2. **Importe os lançamentos**: Use a funcionalidade de importação do sistema para carregar `lancamentos_conciliacao_e_divergencias.csv`
3. **Execute conciliação automática**: Use o botão "Iniciar Conciliação" no menu Conciliação
4. **Verifique divergências**: Acesse o menu Divergências para ver os casos problemáticos
5. **Teste filtros**: Use os filtros para separar registros conciliados e divergentes

## Resultados Esperados

- **Conciliações automáticas**: Aproximadamente 19 pares de registros
- **Divergências detectadas**: Aproximadamente 10+ casos diversos  
- **Registros órfãos**: 2+ casos sem correspondência
- **Total de registros**: 61 registros (30 extratos + 31 lançamentos)

### Cenário 2: Detecção de Divergências
- Importe: `extratos_com_divergencias.csv`
- Importe: `lancamentos_com_divergencias.csv`
- Execute: Conciliação automática
- Resultado esperado: Várias divergências detectadas

### Cenário 3: Dados Complexos
- Importe: `movimentacao_complexa.csv`
- Importe: `lancamentos_complexos.csv`
- Execute: Conciliação automática
- Resultado esperado: Conciliações complexas com observações detalhadas

## Observações

- Todos os valores são fictícios
- Datas concentradas em agosto/setembro de 2025
- Dados criados especificamente para testes
- Incluem diferentes tipos de transações: vendas, compras, impostos, investimentos, etc.
