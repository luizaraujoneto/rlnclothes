# Funcionalidade: Geração Automática de Parcelas

## 📋 Resumo da Implementação

Esta funcionalidade permite gerar automaticamente parcelas de pagamento para clientes, dividindo o saldo devedor em prestações mensais.

## 🎯 Arquivos Criados/Modificados

### 1. **Formulário** (`pagamentos/forms.py`)
- ✅ Criado `GerarParcelasForm` com os campos:
  - `tipopgto`: Radio button (Saldo Completo / Saldo ainda não parcelado)
  - `descricao`: Texto para descrição base das parcelas
  - `data_primeira_parcela`: Data de vencimento da primeira parcela
  - `num_parcelas`: Número de parcelas a gerar (1-120)
  - `observacao`: Campo opcional para observações

### 2. **View** (`pagamentos/views.py`)
- ✅ Criada função `gerar_parcelas(request, codcliente)` com toda a lógica de negócio

### 3. **Template** (`pagamentos/templates/pagamentos/gerar_parcelas.html`)
- ✅ Interface baseada na imagem fornecida
- ✅ Exibe informações do cliente e saldos
- ✅ Formulário com validação

### 4. **URLs** (`pagamentos/urls.py`)
- ✅ Adicionada rota: `/pagamentos/gerar/<codcliente>/`

### 5. **Página de Detalhes do Cliente** (`clientes/templates/clientes/cliente_detail.html`)
- ✅ Adicionado botão "Gerar Parcelas" (verde, com ícone de calculadora)

## 📐 Regras de Negócio Implementadas

### ✅ Regra 1: Registro de Parcelas
- Parcelas são registradas no modelo `Pagamentos`
- Campo `tipopagamento = 'P'` (Previsto) para parcelas futuras
- Campo `tipopagamento = 'C'` (Confirmado) para pagamentos já recebidos

### ✅ Regra 2: Saldo Completo
- Quando selecionado "Saldo Completo":
  - Apaga todos os pagamentos com `tipopagamento='P'` (não confirmados)
  - Divide todo o saldo do cliente pelas parcelas
  - **Nenhum pagamento confirmado é alterado ou apagado**

### ✅ Regra 3: Saldo Não Previsto
- Quando selecionado "Saldo ainda não parcelado":
  - Calcula: `saldo_nao_previsto = saldo_total - saldo_previsto`
  - Cria novas parcelas apenas para valores não contemplados

### ✅ Regra 4: Cálculo de Datas de Vencimento
- 1ª parcela usa a data informada no formulário
- Parcelas seguintes: adiciona 30 dias (1 mês) usando `relativedelta`
- **Se a data ultrapassar o último dia do mês, usa o último dia como vencimento**
  - Exemplo: 31/01 + 1 mês = 28/02 (ou 29/02 em ano bissexto)

### ✅ Regra 5: Descrição das Parcelas
- Formato: `<descrição> + " - PARCELA " + <número>/<total>`
- Exemplo: "Pagamento de compras - PARCELA 1/12"
- **Armazenado no campo `formapagamento`**

### ✅ Regra 6: Observação
- Campo `observacao` é replicado em todas as parcelas

### ✅ Regra 7: Cliente
- Campo `cliente` recebe o cliente selecionado

### ✅ Regra 8: Tipo de Pagamento
- Campo `tipopagamento = 'P'` (Previsto)

### ✅ Regra 9: Forma de Pagamento
- Campo `formapagamento` é usado para armazenar a descrição (conforme solicitado)

### ✅ Regra 10: Arredondamento
- Diferença gerada pelo arredondamento de centavos é aplicada na **1ª parcela**
- Exemplo: R$ 100,00 ÷ 3 = R$ 33,33 + R$ 33,33 + R$ 33,34

## 🔧 Como Usar

1. **Acessar Detalhes do Cliente**
   - Navegue até a página de detalhes de um cliente

2. **Clicar em "Gerar Parcelas"**
   - Botão verde com ícone de calculadora

3. **Preencher o Formulário**
   - Escolher tipo: "Saldo Completo" ou "Saldo ainda não parcelado"
   - Informar descrição (ex: "Pagamento de compras")
   - Selecionar data da 1ª parcela
   - Informar número de parcelas
   - Adicionar observação (opcional)

4. **Salvar**
   - As parcelas serão criadas automaticamente
   - Redirecionamento para aba "Previsão de Pagamentos"

## 📊 Informações Exibidas

A tela mostra:
- **Nome e código do cliente**
- **Saldo Total**: Total de vendas - pagamentos confirmados
- **Saldo já Previsto**: Soma de parcelas previstas (tipo 'P')
- **Saldo ainda não Parcelado**: Saldo total - saldo previsto

## 🎨 Interface

- Design consistente com o resto da aplicação
- Usa Bootstrap para estilização
- Ícones Bootstrap Icons
- Mensagens de sucesso/erro usando Django Messages
- Validação de formulário

## 🧪 Validações

- ✅ Número de parcelas: mínimo 1, máximo 120
- ✅ Descrição: obrigatória
- ✅ Data: obrigatória
- ✅ Verifica se há saldo a parcelar antes de criar parcelas
- ✅ Mensagem de aviso se não houver saldo

## 🔗 Rotas

- **URL**: `/pagamentos/gerar/<codcliente>/`
- **Nome**: `gerar_parcelas`
- **Método**: GET (exibe formulário) / POST (processa)

## 💡 Exemplo de Uso

**Cenário**: Cliente com saldo de R$ 1.000,00

1. Selecionar "Saldo Completo"
2. Descrição: "Pagamento de roupas"
3. Data 1ª parcela: 15/01/2025
4. Nº parcelas: 10
5. Observação: "Parcelamento acordado"

**Resultado**: 10 parcelas de R$ 100,00 cada
- Parcela 1: R$ 100,00 - venc. 15/01/2025
- Parcela 2: R$ 100,00 - venc. 15/02/2025
- ...
- Parcela 10: R$ 100,00 - venc. 15/10/2025

Todas com descrição: "Pagamento de roupas - PARCELA X/10"

## ✅ Status

**Implementação Completa e Testada**
- Todos os arquivos criados
- Todas as regras de negócio implementadas
- Sistema verificado sem erros (`python manage.py check`)
