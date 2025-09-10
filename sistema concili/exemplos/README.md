# Arquivos de Exemplo para Conciliação

Este diretório contém arquivos de exemplo para testar o sistema de conciliação bancária.

## Arquivos Disponíveis

### 1. Dados Principais (Conciliação Completa)
- **extratos_banco_completo.csv**: Extratos bancários completos de setembro/2025
- **lancamentos_contabeis_completo.csv**: Lançamentos contábeis correspondentes

### 2. Dados com Divergências Propositais
- **extratos_com_divergencias.csv**: Extratos de agosto/2025 com inconsistências
- **lancamentos_com_divergencias.csv**: Lançamentos com divergências propositais

### 3. Dados Complexos (Cenário Avançado)
- **movimentacao_complexa.csv**: Movimentações diversas e complexas
- **lancamentos_complexos.csv**: Lançamentos detalhados correspondentes

## Tipos de Divergências Incluídas

1. **Valores Diferentes**: Mesmo documento, valores distintos
2. **Datas Divergentes**: Lançamentos em datas diferentes
3. **Documentos Órfãos**: Extratos sem lançamentos correspondentes
4. **Lançamentos Sem Extrato**: Lançamentos sem correspondência bancária
5. **Descrições Incompatíveis**: Mesmos valores, descrições diferentes
6. **Duplicatas**: Registros duplicados com pequenas variações

## Como Usar

1. **Teste Básico**: Use os arquivos "completo" para testar conciliação normal
2. **Teste de Divergências**: Use os arquivos "com_divergencias" para testar detecção de problemas
3. **Teste Avançado**: Use os arquivos "complexos" para cenários com muitos dados

## Cenários de Teste Recomendados

### Cenário 1: Conciliação Normal
- Importe: `extratos_banco_completo.csv`
- Importe: `lancamentos_contabeis_completo.csv`
- Execute: Conciliação automática
- Resultado esperado: ~80% de conciliações automáticas

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
