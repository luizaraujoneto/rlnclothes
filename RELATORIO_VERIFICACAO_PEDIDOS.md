# Relatório de Verificação de Valores de Pedidos
**Data da Análise:** 10/12/2024

## Resumo Executivo

Foram analisados **384 pedidos** no sistema, verificando se o valor gravado no campo `valorpedido` corresponde à soma dos produtos (para pedidos de compra) ou das devoluções (para pedidos de devolução).

### Resultados Gerais
- **Total de pedidos analisados:** 384
- **Pedidos com divergências (incluindo arredondamento):** 335
- **Pedidos com divergências significativas (> R$ 0,01):** 8
- **Total de diferenças (valor absoluto):** R$ 3.306,56

---

## Divergências Significativas (> R$ 0,01)

### 1. Pedidos com Valor Zerado (6 pedidos)
Estes pedidos têm valor gravado como R$ 0,00, mas possuem produtos associados:

| Número do Pedido | Data       | Tipo   | Valor Gravado | Valor Calculado | Diferença    |
|------------------|------------|--------|---------------|-----------------|--------------|
| NL-R3-2022-07    | 31/07/2022 | Compra | R$ 0,00       | R$ 793,00       | -R$ 793,00   |
| NL-R3-2022-06    | 30/06/2022 | Compra | R$ 0,00       | R$ 950,00       | -R$ 950,00   |
| NL-R3-2022-10    | 30/10/2022 | Compra | R$ 0,00       | R$ 616,30       | -R$ 616,30   |
| NL-R3-2022-11    | 30/11/2022 | Compra | R$ 0,00       | R$ 380,50       | -R$ 380,50   |
| NL-DI-2022-12    | 31/12/2022 | Compra | R$ 0,00       | R$ 214,90       | -R$ 214,90   |
| NL-DI-2022-10    | 31/10/2022 | Compra | R$ 0,00       | R$ 284,00       | -R$ 284,00   |

**Subtotal:** R$ 3.238,70

**Observação:** Estes pedidos parecem ser notas fiscais (NL = Nota?) que não tiveram o valor atualizado corretamente.

---

### 2. Pedidos com Diferenças de Cálculo (2 pedidos)

| Número do Pedido | Data       | Tipo      | Valor Gravado | Valor Calculado | Diferença   |
|------------------|------------|-----------|---------------|-----------------|-------------|
| 1592422          | 21/08/2024 | Compra    | R$ 496,50     | R$ 430,70       | +R$ 65,80   |
| SN-27-11-2024-D  | 27/11/2024 | Devolução | R$ 52,98      | R$ 50,92        | +R$ 2,06    |

**Subtotal:** R$ 67,86

**Observação:** Estes pedidos têm valores gravados diferentes da soma dos produtos. Pode indicar:
- Produtos removidos/alterados após o cálculo inicial
- Ajustes manuais no valor do pedido
- Erros de digitação

---

### 3. Divergências de Arredondamento (327 pedidos)

Os demais 327 pedidos apresentam diferenças de apenas R$ 0,00 (arredondamento de centavos), que são tecnicamente divergências mas não representam problemas reais. Exemplo:
- Valor gravado: R$ 462,30
- Valor calculado: R$ 462,30
- Diferença: +R$ 0,00 ou -R$ 0,00

Estas diferenças são causadas por questões de precisão decimal e não requerem correção.

---

## Recomendações

### Ação Imediata
1. **Investigar os 6 pedidos com valor zerado** (NL-R3-* e NL-DI-*):
   - Verificar se são pedidos válidos
   - Se válidos, executar atualização manual do valor

2. **Revisar os 2 pedidos com diferenças de cálculo**:
   - Pedido 1592422: diferença de R$ 65,80
   - Pedido SN-27-11-2024-D: diferença de R$ 2,06
   - Verificar se houve alterações nos produtos após a criação
   - Verificar se há ajustes manuais justificados

### Ação Preventiva
1. As diferenças de arredondamento (R$ 0,00) podem ser ignoradas ou tratadas com:
   - Ajuste na precisão decimal dos cálculos
   - Normalização dos valores ao salvar

---

## Como Executar a Verificação

### Verificar todos os pedidos:
```bash
python manage.py verificar_valores_pedidos
```

### Verificar apenas divergências significativas (> R$ 0,01):
```bash
python manage.py verificar_valores_pedidos --apenas-significativos
```

---

## Notas Técnicas

- O comando verifica o tipo de pedido (Compra ou Devolução) e busca os produtos no modelo apropriado
- Para pedidos de **Compra (tipo "C")**: soma os valores do modelo `Produtos`
- Para pedidos de **Devolução (tipo "D")**: soma os valores do modelo `Devolucoes`
- Nenhuma alteração foi feita no banco de dados durante esta análise
