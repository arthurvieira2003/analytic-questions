import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os

# Configurando estilo de plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set(font_scale=1.2)
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.facecolor'] = '#f0f0f0'
plt.rcParams['figure.titlesize'] = 16

# Definindo paleta de cores para gráficos
cores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

def carregar_dados(arquivo):
    """Carrega e pré-processa os dados do Titanic."""
    print(f"Carregando dados de {arquivo}...")
    df = pd.read_csv(arquivo, sep=';')
    
    # Verificação de valores nulos
    print("\nValores nulos por coluna:")
    print(df.isnull().sum())
    
    # Conversão de tipos - tratar valores nulos antes da conversão para int
    # Primeiro, vamos garantir que não haja valores nulos em 'survived'
    if df['survived'].isnull().any():
        print(f"Atenção: {df['survived'].isnull().sum()} valores nulos encontrados na coluna 'survived'. Preenchendo com 0.")
        df['survived'] = df['survived'].fillna(0)
    
    # Agora podemos converter com segurança
    df['survived'] = df['survived'].astype(int)
    
    # Tratamento da coluna de idade
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    # Tratamento da coluna fare - primeiro substituir vírgulas por pontos, depois converter
    df['fare'] = df['fare'].str.replace(',', '.').astype(float)
    
    # Criando categorias de idade
    df['categoria_idade'] = pd.cut(
        df['age'],
        bins=[0, 12, 18, 35, 50, 100],
        labels=['Criança (0-12)', 'Adolescente (13-18)', 'Adulto Jovem (19-35)', 'Adulto (36-50)', 'Idoso (50+)']
    )
    
    # Identificando crianças (menos de 18 anos)
    df['is_child'] = df['age'] < 18
    
    return df

def analise_lei_do_mar(df):
    """Análise específica da aplicação da Lei do Mar no desastre do Titanic."""
    
    # 1. Análise por sexo e classe
    sobrevivencia_sexo_classe = df.pivot_table(
        values='survived',
        index='pclass',
        columns='sex',
        aggfunc='mean'
    ).reset_index()
    
    sobrevivencia_sexo_classe.columns.name = None
    sobrevivencia_sexo_classe = sobrevivencia_sexo_classe.rename(
        columns={'female': 'Taxa Mulheres', 'male': 'Taxa Homens'}
    )
    
    # Calcular diferença entre taxas
    sobrevivencia_sexo_classe['Diferença (M-H)'] = (
        sobrevivencia_sexo_classe['Taxa Mulheres'] - sobrevivencia_sexo_classe['Taxa Homens']
    )
    
    # Converter para percentagem
    sobrevivencia_sexo_classe['Taxa Mulheres'] *= 100
    sobrevivencia_sexo_classe['Taxa Homens'] *= 100
    sobrevivencia_sexo_classe['Diferença (M-H)'] *= 100
    
    print("\n1. Taxas de sobrevivência por sexo e classe:")
    print(sobrevivencia_sexo_classe.round(1))
    
    # 2. Análise por faixa etária
    sobrevivencia_idade = df.groupby('categoria_idade')['survived'].agg(['mean', 'count']).reset_index()
    sobrevivencia_idade.columns = ['Faixa Etária', 'Taxa Sobrevivência', 'Total']
    sobrevivencia_idade['Taxa Sobrevivência'] *= 100
    
    print("\n2. Taxas de sobrevivência por faixa etária:")
    print(sobrevivencia_idade.sort_values('Taxa Sobrevivência', ascending=False).round(1))
    
    # 3. Análise por faixa etária e sexo
    sobrevivencia_idade_sexo = df.groupby(['categoria_idade', 'sex'])['survived'].agg(['mean', 'count']).reset_index()
    sobrevivencia_idade_sexo.columns = ['Faixa Etária', 'Sexo', 'Taxa Sobrevivência', 'Total']
    sobrevivencia_idade_sexo['Taxa Sobrevivência'] *= 100
    
    print("\n3. Taxas de sobrevivência por faixa etária e sexo:")
    print(sobrevivencia_idade_sexo.sort_values(['Faixa Etária', 'Taxa Sobrevivência'], ascending=[True, False]).round(1))
    
    # 4. Botes salva-vidas (quando disponível)
    df_botes = df.dropna(subset=['boat'])
    
    # Contagem de pessoas em botes por sexo
    pessoas_botes = df_botes.groupby('sex').size().reset_index(name='Total em Botes')
    total_por_sexo = df.groupby('sex').size().reset_index(name='Total no Navio')
    
    pessoas_botes = pd.merge(pessoas_botes, total_por_sexo, on='sex')
    pessoas_botes['Percentual em Botes'] = pessoas_botes['Total em Botes'] / pessoas_botes['Total no Navio'] * 100
    
    print("\n4. Distribuição de pessoas em botes salva-vidas por sexo:")
    print(pessoas_botes.round(1))
    
    # 5. Capacidade dos botes vs. número de passageiros
    total_passageiros = len(df)
    total_sobreviventes = df['survived'].sum()
    
    print(f"\n5. Capacidade de resgate:")
    print(f"   Total de passageiros: {total_passageiros}")
    print(f"   Total de sobreviventes: {total_sobreviventes}")
    print(f"   Percentual de resgate: {total_sobreviventes/total_passageiros*100:.1f}%")
    
    # Criar visualizações
    figuras = []
    
    # Figura 1: Sobrevivência por sexo e classe
    fig1, ax1 = plt.subplots()
    df_plot = pd.melt(
        sobrevivencia_sexo_classe, 
        id_vars=['pclass'], 
        value_vars=['Taxa Mulheres', 'Taxa Homens'],
        var_name='Sexo', 
        value_name='Taxa de Sobrevivência (%)'
    )
    sns.barplot(x='pclass', y='Taxa de Sobrevivência (%)', hue='Sexo', data=df_plot, palette=[cores[1], cores[0]], ax=ax1)
    ax1.set_title('Taxa de Sobrevivência por Classe e Sexo')
    ax1.set_xlabel('Classe')
    ax1.set_ylabel('Taxa de Sobrevivência (%)')
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax1.patches):
        ax1.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10, color='black')
    
    figuras.append(fig1)
    
    # Figura 2: Sobrevivência por faixa etária
    fig2, ax2 = plt.subplots()
    sobrevivencia_idade_ordenada = sobrevivencia_idade.sort_values('Faixa Etária')
    sns.barplot(x='Faixa Etária', y='Taxa Sobrevivência', data=sobrevivencia_idade_ordenada, palette=cores, ax=ax2)
    ax2.set_title('Taxa de Sobrevivência por Faixa Etária')
    ax2.set_xlabel('Faixa Etária')
    ax2.set_ylabel('Taxa de Sobrevivência (%)')
    plt.xticks(rotation=45)
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax2.patches):
        ax2.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10, color='black')
    
    figuras.append(fig2)
    
    # Figura 3: Sobrevivência por faixa etária e sexo
    fig3, ax3 = plt.subplots()
    df_plot = sobrevivencia_idade_sexo.copy()
    df_plot['Sexo'] = df_plot['Sexo'].map({'male': 'Homens', 'female': 'Mulheres'})
    sns.barplot(x='Faixa Etária', y='Taxa Sobrevivência', hue='Sexo', data=df_plot, palette=[cores[0], cores[1]], ax=ax3)
    ax3.set_title('Taxa de Sobrevivência por Faixa Etária e Sexo')
    ax3.set_xlabel('Faixa Etária')
    ax3.set_ylabel('Taxa de Sobrevivência (%)')
    plt.xticks(rotation=45)
    plt.legend(title='Sexo')
    
    figuras.append(fig3)
    
    # Figura 4: Percentual de pessoas em botes por sexo
    fig4, ax4 = plt.subplots()
    pessoas_botes['Sexo'] = pessoas_botes['sex'].map({'male': 'Homens', 'female': 'Mulheres'})
    sns.barplot(x='Sexo', y='Percentual em Botes', data=pessoas_botes, palette=[cores[0], cores[1]], ax=ax4)
    ax4.set_title('Percentual de Pessoas em Botes Salva-vidas por Sexo')
    ax4.set_xlabel('Sexo')
    ax4.set_ylabel('Percentual em Botes (%)')
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax4.patches):
        ax4.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10, color='black')
    
    figuras.append(fig4)
    
    # Figura 5: Análise de capacidade de resgate
    fig5, ax5 = plt.subplots()
    labels = ['Sobreviventes', 'Não Sobreviventes']
    sizes = [total_sobreviventes, total_passageiros - total_sobreviventes]
    explode = (0.1, 0)
    ax5.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, colors=[cores[2], cores[1]])
    ax5.set_title('Proporção de Sobreviventes no Titanic')
    ax5.axis('equal')
    
    figuras.append(fig5)
    
    return figuras, sobrevivencia_sexo_classe, sobrevivencia_idade, sobrevivencia_idade_sexo, pessoas_botes

def conclusoes_lei_do_mar(sobrev_sex_classe, sobrev_idade, sobrev_idade_sexo, pessoas_botes):
    """Gera conclusões específicas sobre a aplicação da Lei do Mar no Titanic."""
    
    print("\n=== CONCLUSÕES SOBRE A LEI DO MAR NO TITANIC ===")
    
    # 1. Análise da prioridade por sexo
    taxa_mulheres = sobrev_sex_classe['Taxa Mulheres'].mean()
    taxa_homens = sobrev_sex_classe['Taxa Homens'].mean()
    
    print(f"\n1. Prioridade para mulheres:")
    print(f"   - Taxa média de sobrevivência de mulheres: {taxa_mulheres:.1f}%")
    print(f"   - Taxa média de sobrevivência de homens: {taxa_homens:.1f}%")
    
    if taxa_mulheres > taxa_homens:
        diferenca = taxa_mulheres / taxa_homens
        print(f"   - Mulheres tiveram {diferenca:.1f}x mais chances de sobreviver que homens")
        print("   - Há evidência clara de prioridade para mulheres")
    else:
        print("   - Não há evidência de prioridade para mulheres")
    
    # 2. Análise da prioridade por idade
    criancas = sobrev_idade[sobrev_idade['Faixa Etária'].isin(['Criança (0-12)', 'Adolescente (13-18)'])]
    taxa_criancas = criancas['Taxa Sobrevivência'].mean()
    
    adultos = sobrev_idade[~sobrev_idade['Faixa Etária'].isin(['Criança (0-12)', 'Adolescente (13-18)'])]
    taxa_adultos = adultos['Taxa Sobrevivência'].mean()
    
    print(f"\n2. Prioridade para crianças:")
    print(f"   - Taxa média de sobrevivência de crianças/adolescentes: {taxa_criancas:.1f}%")
    print(f"   - Taxa média de sobrevivência de adultos: {taxa_adultos:.1f}%")
    
    if taxa_criancas > taxa_adultos:
        diferenca = taxa_criancas / taxa_adultos
        print(f"   - Crianças tiveram {diferenca:.1f}x mais chances de sobreviver que adultos")
        print("   - Há evidência de prioridade para crianças")
    else:
        print("   - Não há evidência consistente de prioridade para crianças")
    
    # 3. Verificação de consistência entre classes
    print("\n3. Consistência entre classes socioeconômicas:")
    for pclass in [1, 2, 3]:
        tx_mulheres = sobrev_sex_classe[sobrev_sex_classe['pclass'] == pclass]['Taxa Mulheres'].values[0]
        tx_homens = sobrev_sex_classe[sobrev_sex_classe['pclass'] == pclass]['Taxa Homens'].values[0]
        diferenca = sobrev_sex_classe[sobrev_sex_classe['pclass'] == pclass]['Diferença (M-H)'].values[0]
        
        print(f"   - Classe {pclass}:")
        print(f"     * Mulheres: {tx_mulheres:.1f}%, Homens: {tx_homens:.1f}%")
        print(f"     * Diferença: {diferenca:.1f} pontos percentuais")
    
    # 4. Análise das pessoas em botes
    tx_mulheres_botes = pessoas_botes[pessoas_botes['sex'] == 'female']['Percentual em Botes'].values[0]
    tx_homens_botes = pessoas_botes[pessoas_botes['sex'] == 'male']['Percentual em Botes'].values[0]
    
    print(f"\n4. Acesso aos botes salva-vidas:")
    print(f"   - Percentual de mulheres que acessaram botes: {tx_mulheres_botes:.1f}%")
    print(f"   - Percentual de homens que acessaram botes: {tx_homens_botes:.1f}%")
    
    # 5. Conclusão final sobre a Lei do Mar
    print("\n5. Conclusão sobre a afirmação do artigo:")
    print("   Com base na análise dos dados, podemos concluir que:")
    
    if taxa_mulheres > taxa_homens and all(sobrev_sex_classe['Taxa Mulheres'] > sobrev_sex_classe['Taxa Homens']):
        print("   - A tripulação do Titanic priorizou o resgate de mulheres em todas as classes")
    else:
        print("   - A prioridade para mulheres não foi consistente em todas as classes")
    
    if taxa_criancas > taxa_adultos:
        print("   - Há evidência de que crianças tiveram prioridade sobre adultos")
    else:
        print("   - Não há evidência consistente de prioridade para crianças")
    
    # Verificar se classe social teve impacto significativo
    classe1 = sobrev_sex_classe[sobrev_sex_classe['pclass'] == 1][['Taxa Mulheres', 'Taxa Homens']].mean().mean()
    classe3 = sobrev_sex_classe[sobrev_sex_classe['pclass'] == 3][['Taxa Mulheres', 'Taxa Homens']].mean().mean()
    diferenca_classes = classe1 - classe3
    
    if diferenca_classes > 20:  # diferença de 20 pontos percentuais ou mais
        print(f"   - A classe social teve impacto significativo na sobrevivência (diferença de {diferenca_classes:.1f} pontos percentuais)")
        print("   - A 'Lei do Mar' parece ter sido aplicada de forma desigual entre as classes sociais")
        print("   - O status socioeconômico influenciou significativamente nas chances de sobrevivência")
    
    print("\n   CONCLUSÃO FINAL:")
    if taxa_mulheres > taxa_homens and taxa_criancas > taxa_adultos:
        print("   A afirmação de que 'A tripulação do Titanic seguiu a Lei do Mar' é parcialmente verdadeira,")
        print("   pois mulheres e crianças tiveram maior probabilidade de sobrevivência.")
    else:
        print("   A afirmação de que 'A tripulação do Titanic seguiu a Lei do Mar' não é inteiramente precisa,")
    
    if diferenca_classes > 20:
        print("   pois a aplicação dessa prioridade foi significativamente influenciada pela classe socioeconômica.")
    else:
        print("   pois não houve aplicação consistente da prioridade para crianças em todas as circunstâncias.")

def main():
    # Carregar dados
    df = carregar_dados("titanic3.csv")
    
    # Realizar análise
    figuras, sobrev_sex_classe, sobrev_idade, sobrev_idade_sexo, pessoas_botes = analise_lei_do_mar(df)
    
    # Gerar conclusões
    conclusoes_lei_do_mar(sobrev_sex_classe, sobrev_idade, sobrev_idade_sexo, pessoas_botes)
    
    # Remover o arquivo PDF antigo se ele existir
    output_pdf = 'lei_do_mar_titanic.pdf'
    if os.path.exists(output_pdf):
        try:
            os.remove(output_pdf)
            print(f"Arquivo antigo {output_pdf} removido com sucesso.")
        except Exception as e:
            print(f"Não foi possível remover o arquivo antigo: {e}")
    
    # Salvar gráficos em PDF
    try:
        with PdfPages(output_pdf) as pdf:
            for i, fig in enumerate(figuras):
                pdf.savefig(fig)
                
        # Fechar todas as figuras para liberar memória
        for fig in figuras:
            plt.close(fig)
            
        print(f"\nAnálise concluída. Os resultados foram salvos em '{output_pdf}'")
    except Exception as e:
        print(f"\nErro ao salvar o PDF: {e}")
        print("Tentando salvar as figuras individualmente como arquivos PNG...")
        
        # Plano B: Salvar figuras individuais como PNG se o PDF falhar
        nomes_figuras = ['classe_sexo', 'faixa_etaria', 'faixa_etaria_sexo', 'botes_sexo', 'proporcao_sobreviventes']
        for i, fig in enumerate(figuras):
            nome_arquivo = f"lei_do_mar_{nomes_figuras[i] if i < len(nomes_figuras) else i}.png"
            fig.savefig(nome_arquivo)
            print(f"Figura salva como {nome_arquivo}")
            plt.close(fig)
        
        print("Figuras salvas como arquivos PNG separados.")

if __name__ == "__main__":
    main() 