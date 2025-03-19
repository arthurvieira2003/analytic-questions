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

# Definindo paleta de cores para gráficos
cores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

# Função para carregar e pré-processar dados
def carregar_dados(arquivo):
    print(f"Carregando dados de {arquivo}...")
    # Carregamento dos dados
    df = pd.read_csv(arquivo, sep=';')
    
    # Visualização inicial dos dados
    print("\nInformações do Dataset:")
    print(f"Número de registros: {df.shape[0]}")
    print(f"Número de colunas: {df.shape[1]}")
    
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
    
    # Criando coluna para classificar como criança (menos de 18 anos)
    df['is_child'] = df['age'] < 18
    
    # Convertendo valores de fare (tarifa) para numérico
    df['fare'] = df['fare'].str.replace(',', '.').astype(float)
    
    return df

# Função para analisar taxa de sobrevivência por sexo
def analisar_sobrevivencia_por_sexo(df):
    print("\nAnálise de sobrevivência por sexo:")
    sobrev_sexo = df.groupby('sex')['survived'].mean().reset_index()
    total_por_sexo = df.groupby('sex').size().reset_index(name='total')
    
    sobrev_sexo = pd.merge(sobrev_sexo, total_por_sexo, on='sex')
    sobrev_sexo['survived_count'] = (sobrev_sexo['survived'] * sobrev_sexo['total']).astype(int)
    sobrev_sexo['taxa_sobrevivencia'] = sobrev_sexo['survived'] * 100
    
    print(sobrev_sexo[['sex', 'taxa_sobrevivencia', 'survived_count', 'total']])
    
    fig, ax = plt.subplots()
    sns.barplot(x='sex', y='taxa_sobrevivencia', data=sobrev_sexo, palette=[cores[0], cores[1]], ax=ax)
    ax.set_title('Taxa de Sobrevivência por Sexo')
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Taxa de Sobrevivência (%)')
    ax.set_xticklabels(['Masculino', 'Feminino'])
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=12, color='black')
    
    return fig, sobrev_sexo

# Função para analisar taxa de sobrevivência por idade (crianças vs adultos)
def analisar_sobrevivencia_por_idade(df):
    print("\nAnálise de sobrevivência por idade (crianças vs adultos):")
    # Remover registros sem idade definida
    df_idade = df.dropna(subset=['age'])
    
    sobrev_idade = df_idade.groupby('is_child')['survived'].mean().reset_index()
    total_por_idade = df_idade.groupby('is_child').size().reset_index(name='total')
    
    sobrev_idade = pd.merge(sobrev_idade, total_por_idade, on='is_child')
    sobrev_idade['survived_count'] = (sobrev_idade['survived'] * sobrev_idade['total']).astype(int)
    sobrev_idade['taxa_sobrevivencia'] = sobrev_idade['survived'] * 100
    
    sobrev_idade['categoria'] = sobrev_idade['is_child'].map({True: 'Crianças (<18)', False: 'Adultos (≥18)'})
    
    print(sobrev_idade[['categoria', 'taxa_sobrevivencia', 'survived_count', 'total']])
    
    fig, ax = plt.subplots()
    sns.barplot(x='categoria', y='taxa_sobrevivencia', data=sobrev_idade, palette=[cores[2], cores[3]], ax=ax)
    ax.set_title('Taxa de Sobrevivência por Idade')
    ax.set_xlabel('Categoria de Idade')
    ax.set_ylabel('Taxa de Sobrevivência (%)')
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=12, color='black')
    
    return fig, sobrev_idade

# Função para analisar taxa de sobrevivência por classe
def analisar_sobrevivencia_por_classe(df):
    print("\nAnálise de sobrevivência por classe:")
    sobrev_classe = df.groupby('pclass')['survived'].mean().reset_index()
    total_por_classe = df.groupby('pclass').size().reset_index(name='total')
    
    sobrev_classe = pd.merge(sobrev_classe, total_por_classe, on='pclass')
    sobrev_classe['survived_count'] = (sobrev_classe['survived'] * sobrev_classe['total']).astype(int)
    sobrev_classe['taxa_sobrevivencia'] = sobrev_classe['survived'] * 100
    
    print(sobrev_classe[['pclass', 'taxa_sobrevivencia', 'survived_count', 'total']])
    
    fig, ax = plt.subplots()
    sns.barplot(x='pclass', y='taxa_sobrevivencia', data=sobrev_classe, palette=cores[:3], ax=ax)
    ax.set_title('Taxa de Sobrevivência por Classe')
    ax.set_xlabel('Classe')
    ax.set_ylabel('Taxa de Sobrevivência (%)')
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=12, color='black')
    
    return fig, sobrev_classe

# Função para análise cruzada: classe, sexo e taxa de sobrevivência
def analisar_sobrevivencia_classe_sexo(df):
    print("\nAnálise cruzada de sobrevivência por classe e sexo:")
    sobrev_classe_sexo = df.groupby(['pclass', 'sex'])['survived'].mean().reset_index()
    total_por_classe_sexo = df.groupby(['pclass', 'sex']).size().reset_index(name='total')
    
    sobrev_classe_sexo = pd.merge(sobrev_classe_sexo, total_por_classe_sexo, on=['pclass', 'sex'])
    sobrev_classe_sexo['survived_count'] = (sobrev_classe_sexo['survived'] * sobrev_classe_sexo['total']).astype(int)
    sobrev_classe_sexo['taxa_sobrevivencia'] = sobrev_classe_sexo['survived'] * 100
    
    print(sobrev_classe_sexo[['pclass', 'sex', 'taxa_sobrevivencia', 'survived_count', 'total']])
    
    fig, ax = plt.subplots()
    sns.barplot(x='pclass', y='taxa_sobrevivencia', hue='sex', data=sobrev_classe_sexo, palette=[cores[0], cores[1]], ax=ax)
    ax.set_title('Taxa de Sobrevivência por Classe e Sexo')
    ax.set_xlabel('Classe')
    ax.set_ylabel('Taxa de Sobrevivência (%)')
    ax.legend(title='Sexo', labels=['Masculino', 'Feminino'])
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10, color='black')
    
    return fig, sobrev_classe_sexo

# Função para análise cruzada: classe, idade (criança/adulto) e taxa de sobrevivência
def analisar_sobrevivencia_classe_idade(df):
    print("\nAnálise cruzada de sobrevivência por classe e idade:")
    # Remover registros sem idade definida
    df_idade = df.dropna(subset=['age'])
    
    sobrev_classe_idade = df_idade.groupby(['pclass', 'is_child'])['survived'].mean().reset_index()
    total_por_classe_idade = df_idade.groupby(['pclass', 'is_child']).size().reset_index(name='total')
    
    sobrev_classe_idade = pd.merge(sobrev_classe_idade, total_por_classe_idade, on=['pclass', 'is_child'])
    sobrev_classe_idade['survived_count'] = (sobrev_classe_idade['survived'] * sobrev_classe_idade['total']).astype(int)
    sobrev_classe_idade['taxa_sobrevivencia'] = sobrev_classe_idade['survived'] * 100
    
    sobrev_classe_idade['categoria'] = sobrev_classe_idade['is_child'].map({True: 'Crianças (<18)', False: 'Adultos (≥18)'})
    
    print(sobrev_classe_idade[['pclass', 'categoria', 'taxa_sobrevivencia', 'survived_count', 'total']])
    
    fig, ax = plt.subplots()
    sns.barplot(x='pclass', y='taxa_sobrevivencia', hue='categoria', data=sobrev_classe_idade, palette=[cores[2], cores[3]], ax=ax)
    ax.set_title('Taxa de Sobrevivência por Classe e Idade')
    ax.set_xlabel('Classe')
    ax.set_ylabel('Taxa de Sobrevivência (%)')
    
    # Adicionar rótulos de porcentagem
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10, color='black')
    
    return fig, sobrev_classe_idade

# Função principal para executar todas as análises
def analisar_dados_titanic(arquivo):
    # Carregar e processar os dados
    df = carregar_dados(arquivo)
    
    # Remover o arquivo PDF antigo se ele existir
    output_pdf = 'analise_titanic.pdf'
    if os.path.exists(output_pdf):
        try:
            os.remove(output_pdf)
            print(f"Arquivo antigo {output_pdf} removido com sucesso.")
        except Exception as e:
            print(f"Não foi possível remover o arquivo antigo: {e}")
    
    # Criar figuras individualmente
    fig_sexo, dados_sexo = analisar_sobrevivencia_por_sexo(df)
    fig_idade, dados_idade = analisar_sobrevivencia_por_idade(df)
    fig_classe, dados_classe = analisar_sobrevivencia_por_classe(df)
    fig_classe_sexo, dados_classe_sexo = analisar_sobrevivencia_classe_sexo(df)
    fig_classe_idade, dados_classe_idade = analisar_sobrevivencia_classe_idade(df)
    
    # Gerar conclusões baseadas nos dados
    gerar_conclusoes(dados_sexo, dados_idade, dados_classe_sexo, dados_classe_idade)
    
    # Salvar figuras em PDF após todas as análises estarem concluídas
    try:
        with PdfPages(output_pdf) as pdf:
            pdf.savefig(fig_sexo)
            pdf.savefig(fig_idade)
            pdf.savefig(fig_classe)
            pdf.savefig(fig_classe_sexo)
            pdf.savefig(fig_classe_idade)
            
        # Fechar todas as figuras para liberar memória
        plt.close(fig_sexo)
        plt.close(fig_idade)
        plt.close(fig_classe)
        plt.close(fig_classe_sexo)
        plt.close(fig_classe_idade)
        
        print(f"\nAnálise concluída. Os resultados foram salvos em '{output_pdf}'")
    except Exception as e:
        print(f"\nErro ao salvar o PDF: {e}")
        print("Tentando salvar as figuras individualmente como arquivos PNG...")
        
        # Plano B: Salvar figuras individuais como PNG se o PDF falhar
        fig_sexo.savefig('sobrevivencia_por_sexo.png')
        fig_idade.savefig('sobrevivencia_por_idade.png')
        fig_classe.savefig('sobrevivencia_por_classe.png')
        fig_classe_sexo.savefig('sobrevivencia_por_classe_e_sexo.png')
        fig_classe_idade.savefig('sobrevivencia_por_classe_e_idade.png')
        
        print("Figuras salvas como arquivos PNG separados.")
        
        # Fechar todas as figuras
        plt.close('all')

# Função para gerar conclusões baseadas nos dados analisados
def gerar_conclusoes(dados_sexo, dados_idade, dados_classe_sexo, dados_classe_idade):
    print("\n=== CONCLUSÕES DA ANÁLISE ===")
    
    # Conclusão sobre taxa de sobrevivência por sexo
    taxa_mulheres = dados_sexo[dados_sexo['sex'] == 'female']['taxa_sobrevivencia'].values[0]
    taxa_homens = dados_sexo[dados_sexo['sex'] == 'male']['taxa_sobrevivencia'].values[0]
    
    print(f"\n1. Taxa de sobrevivência por sexo:")
    print(f"   - Mulheres: {taxa_mulheres:.1f}%")
    print(f"   - Homens: {taxa_homens:.1f}%")
    print(f"   - As mulheres tiveram {taxa_mulheres/taxa_homens:.1f} vezes mais chances de sobreviver que os homens")
    
    # Conclusão sobre taxa de sobrevivência por idade
    taxa_criancas = dados_idade[dados_idade['is_child'] == True]['taxa_sobrevivencia'].values[0]
    taxa_adultos = dados_idade[dados_idade['is_child'] == False]['taxa_sobrevivencia'].values[0]
    
    print(f"\n2. Taxa de sobrevivência por idade:")
    print(f"   - Crianças (<18 anos): {taxa_criancas:.1f}%")
    print(f"   - Adultos (≥18 anos): {taxa_adultos:.1f}%")
    print(f"   - As crianças tiveram {taxa_criancas/taxa_adultos:.1f} vezes mais chances de sobreviver que os adultos")
    
    # Conclusão sobre taxa de sobrevivência por classe e sexo
    print("\n3. Taxa de sobrevivência por classe e sexo:")
    for classe in [1, 2, 3]:
        dados_classe = dados_classe_sexo[dados_classe_sexo['pclass'] == classe]
        taxa_m = dados_classe[dados_classe['sex'] == 'female']['taxa_sobrevivencia'].values[0]
        taxa_h = dados_classe[dados_classe['sex'] == 'male']['taxa_sobrevivencia'].values[0]
        print(f"   - Classe {classe}:")
        print(f"     * Mulheres: {taxa_m:.1f}%")
        print(f"     * Homens: {taxa_h:.1f}%")
    
    # Análise da "Lei do Mar" (mulheres e crianças primeiro)
    print("\n4. Avaliação sobre a 'Lei do Mar' (mulheres e crianças primeiro):")
    
    # Verificar se a taxa de sobrevivência de mulheres é maior que homens em todas as classes
    # Corrigindo a comparação para evitar o erro de Series com índices diferentes
    mulheres_maior_taxa = True
    for classe in sorted(dados_classe_sexo['pclass'].unique()):
        dados_classe = dados_classe_sexo[dados_classe_sexo['pclass'] == classe]
        taxa_m = dados_classe[dados_classe['sex'] == 'female']['taxa_sobrevivencia'].values[0]
        taxa_h = dados_classe[dados_classe['sex'] == 'male']['taxa_sobrevivencia'].values[0]
        if taxa_m <= taxa_h:
            mulheres_maior_taxa = False
            break
    
    if mulheres_maior_taxa:
        print("   - Os dados mostram que mulheres tiveram maior taxa de sobrevivência em todas as classes")
    else:
        print("   - Não há evidência consistente de que mulheres tiveram prioridade em todas as classes")
        
    if taxa_criancas > taxa_adultos:
        print("   - Os dados mostram que crianças tiveram maior taxa de sobrevivência que adultos")
    else:
        print("   - Não há evidência de que crianças tiveram prioridade sobre adultos")
    
    # Conclusão geral sobre a Lei do Mar
    print("\n5. Conclusão sobre a afirmação do artigo:")
    print("   Com base nos dados analisados, podemos observar que:")
    print("   - Mulheres tiveram prioridade clara sobre homens")
    print("   - O status socioeconômico (classe) parece ter influenciado significativamente as chances de sobrevivência")
    print("   - A hipótese de que 'a tripulação do Titanic seguiu a Lei do Mar' é parcialmente suportada,")
    print("     mas com influência significativa de fatores socioeconômicos")

if __name__ == "__main__":
    # Executar a análise com o arquivo CSV do Titanic
    analisar_dados_titanic("titanic3.csv") 