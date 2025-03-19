# Análise do Naufrágio do Titanic

Este projeto realiza uma análise dos dados do Titanic para verificar se a tripulação seguiu a "Lei do Mar" durante o desastre, que estabelece prioridade de resgate para mulheres e crianças.

## Acadêmicos

Arthur Henrique Tscha Vieira e Rafael Rodrigues Ferreira de Andrade.

## Objetivo

Verificar a afirmação: "A tripulação do Titanic seguiu a Lei do Mar ao responder ao desastre".

A Lei do Mar é um princípio marítimo não escrito que estabelece que, em situações de emergência, a prioridade de resgate deve ser dada a passageiros mais vulneráveis, especificamente mulheres e crianças.

## Metodologia

Foi realizada uma análise dos dados de 1.309 passageiros do Titanic, examinando as taxas de sobrevivência por:

- Sexo (homens vs. mulheres)
- Idade (crianças vs. adultos)
- Classe socioeconômica (1ª, 2ª e 3ª classes)
- Combinações desses fatores

## Perguntas Respondidas

1. Qual é a taxa de sobrevivência das mulheres e como ela se compara à taxa de sobrevivência dos homens?
2. Qual é a taxa de sobrevivência das crianças e como ela se compara à taxa de sobrevivência dos adultos?
3. Quais são as taxas de sobrevivência de homens, mulheres e crianças discriminadas por classe?

## Resultados Principais

### 1. Sobrevivência por Sexo

- **Mulheres**: Taxa de sobrevivência significativamente maior do que homens em todas as classes
- As mulheres tiveram, em média, aproximadamente 3-4 vezes mais chances de sobreviver que os homens

### 2. Sobrevivência por Idade

- **Crianças**: Taxa de sobrevivência maior que adultos
- A prioridade para crianças foi menos consistente do que para mulheres

### 3. Sobrevivência por Classe Social

- **1ª Classe**: Taxas de sobrevivência significativamente maiores do que as outras classes
- **3ª Classe**: Taxas de sobrevivência significativamente menores, mesmo entre mulheres e crianças
- Diferença entre 1ª e 3ª classe: aproximadamente 30-40 pontos percentuais

### 4. Análise Cruzada por Sexo e Classe

| Classe | Mulheres | Homens | Diferença |
| ------ | -------- | ------ | --------- |
| 1ª     | ~95%     | ~35%   | ~60%      |
| 2ª     | ~90%     | ~15%   | ~75%      |
| 3ª     | ~50%     | ~15%   | ~35%      |

_Nota: Valores aproximados baseados na análise dos dados_

### 5. Acesso aos Botes Salva-vidas

- Mulheres tiveram acesso prioritário aos botes em todas as classes
- A capacidade total dos botes era insuficiente para acomodar todos os passageiros
- Os dados mostram que apenas cerca de 30-35% dos passageiros sobreviveram

## Conclusões

Com base na análise dos dados, podemos concluir que:

1. **A Lei do Mar foi parcialmente seguida pela tripulação do Titanic**:

   - Mulheres receberam prioridade clara sobre homens em todas as classes
   - Crianças tiveram alguma prioridade, mas de forma menos consistente

2. **A classe socioeconômica teve influência significativa**:

   - Passageiros da 1ª classe tiveram taxas de sobrevivência muito maiores do que os da 3ª classe
   - Mesmo entre mulheres, a classe social foi um fator determinante (95% na 1ª classe vs. 50% na 3ª classe)

3. **A afirmação de que "a tripulação do Titanic seguiu a Lei do Mar" é parcialmente precisa**:
   - A tripulação priorizou mulheres, o que corresponde à Lei do Mar
   - No entanto, a aplicação deste princípio foi fortemente influenciada pela classe socioeconômica
   - A prioridade para crianças foi menos evidente nos dados

## Scripts Disponíveis

### 1. Análise Geral (analise_titanic.py)

Realiza uma análise geral dos dados do Titanic com foco nas taxas de sobrevivência por sexo, idade e classe.

Funcionalidades específicas:

- Análise de sobrevivência por sexo (homens vs. mulheres)
- Análise de sobrevivência por idade (crianças vs. adultos)
- Análise de sobrevivência por classe (1ª, 2ª e 3ª classe)
- Análise cruzada por classe e sexo
- Análise cruzada por classe e idade
- Geração de gráficos de barras comparativos
- Criação de relatório em PDF com resultados visuais

### 2. Análise da Lei do Mar (lei_do_mar_titanic.py)

Foca especificamente na verificação da aplicação da "Lei do Mar" no desastre, incluindo:

- Análise detalhada por faixas etárias (0-12, 13-18, 19-35, 36-50, 50+)
- Comparação das taxas de sobrevivência entre classes sociais
- Verificação da distribuição de pessoas nos botes salva-vidas
- Avaliação da consistência da aplicação da "Lei do Mar" entre diferentes grupos
- Análise estatística do impacto da classe social no acesso aos botes salva-vidas
- Geração de visualizações mais detalhadas

## Como Executar

1. Certifique-se de ter o Python instalado (versão 3.6 ou superior)

2. Instale as dependências:

   ```
   pip install pandas numpy matplotlib seaborn
   ```

3. Execute o script desejado:

   ```
   python analise_titanic.py
   ```

   ou

   ```
   python lei_do_mar_titanic.py
   ```

4. Os resultados serão exibidos no console e arquivos PDF com os gráficos serão gerados:

   - `analise_titanic.pdf`: Contém os gráficos da análise geral
   - `lei_do_mar_titanic.pdf`: Contém visualizações específicas sobre a análise da Lei do Mar

   Se houver problemas com a geração do PDF, os gráficos serão salvos automaticamente como arquivos PNG individuais.

## Solução de Problemas

- **Erro de valores nulos**: O código trata automaticamente valores nulos na coluna 'survived', preenchendo-os com 0
- **Erro no PDF**: Se o PDF não puder ser aberto, os gráficos serão salvos como arquivos PNG separados
- **Problema de formato**: O dataset usa ponto-e-vírgula como separador e vírgula para decimais, o que é tratado automaticamente no código

## Dataset

O dataset utilizado (`titanic3.csv`) contém informações sobre 1.309 passageiros do Titanic, incluindo:

- **pclass**: Classe (1 = 1ª classe, 2 = 2ª classe, 3 = 3ª classe)
- **survived**: Sobrevivência (1 = sobreviveu, 0 = não sobreviveu)
- **name**: Nome do passageiro
- **sex**: Sexo (male = masculino, female = feminino)
- **age**: Idade em anos (frações indicam menos de 1 ano)
- **sibsp**: Número de irmãos/cônjuges a bordo
- **parch**: Número de pais/filhos a bordo
- **ticket**: Número do bilhete
- **fare**: Tarifa paga (em libras)
- **cabin**: Número da cabine
- **embarked**: Porto de embarque (C = Cherbourg, Q = Queenstown, S = Southampton)
- **boat**: Número do bote salva-vidas (quando disponível)
- **body**: Número de identificação do corpo (quando recuperado)
- **home.dest**: Destino/Residência

---

**Análise baseada em:** Dataset titanic3.csv (1.309 passageiros)
