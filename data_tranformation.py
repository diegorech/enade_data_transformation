# Enade Data Transformation - Aula 3 Módulo 1 Bootcamp IGTI Engenharia de Dados

import pandas as pd
import numpy as np
import os



enade_df = pd.read_csv(
    './../enade_data_extraction/enade2019/microdados_enade_2019/2019/3.DADOS/microdados_enade_2019.txt',
    sep = ';',
    decimal = ','
) 


##############################################################################################################################################################################
################################################################### Analises iniciais ###################################################################################

# Primeiras 5 linhas
print(enade_df.head())

# Verificando a tipagem dos dados da tabela
print(dict(enade_df.dtypes))


'''
    Colunas que serão selecionadas do dataframe
    - CO_IES: Código da Instituição de ensino    
    - CO_CATEGAD: Categoria admnistratica
    - CO_GRUPO: Categoria do grupo
    - CO_MODALIDADE: Se é presencial ou EAD
    - CO_UF_CURSO 
    - CO_REGIAO_CURSO 
    - NU_IDADE 
    - TP_SEXO
    - NT_GER: Nota geral
    - NT_FG: Nota da formação geral
    - NT_CE: Nota do componente específico 

    E alguns itens do questionário:

    - 01: Estado Civil
    - 02: Cor ou raça
    - 04: Escolaridade do pai
    - 05: Escolaridade da mãe
    - 08: Renda familiar
    - 10: Situação de trabalho
    - 11: Situação de bolsa
    - 14: intercâmbio 
    - 15: Cotas
    - 23: Horas de estudo por semana
    - 25: Motivo de escolha do curso
    - 26: Motivo de escolha da estituição de ensino superior
'''


print('\nInformações sobre: Dataframe')
print(enade_df.shape)
# NT_GER
print('\nInformações sobre: Notas Gerais')
print(enade_df.NT_GER.describe())


# Contar o número de nulos
NT_GER_TOTAL_NULLS = enade_df.NT_GER.isnull().sum()
print('Total de notas gerais nulas: ',NT_GER_TOTAL_NULLS)

# Porcentagem de nulos em relação ao total de linhas

print(f'% de notas gerais nulas em relação ao total: \n{round((NT_GER_TOTAL_NULLS / enade_df.shape[0]) * 100, 2)}%')


# .loc filtra linhas do dataframe por um condição
# CO_REGIAO_CURSO == 2 representa os alunos do Nordetes
print('\nInformações sobre: Nota Geral de alunos da Região Nordeste')
print(enade_df.loc[
    enade_df.CO_REGIAO_CURSO == 2
].NT_GER.describe())

# Excluindo notas 0
print('\nInformações sobre: Notas gerais maiores que 0')
print(enade_df.loc[
    enade_df.NT_GER > 0
].NT_GER.describe())

print('\nInformações sobre: Nota Geral de alunos com idade entre 20 e 50 anos')
print(enade_df.loc[
    (enade_df.NU_IDADE >= 20) &
    (enade_df.NU_IDADE <= 50) 
].NT_GER.describe())


# Tabela Cruzada
# Contar quantos homens e mulheres
print('\nInformações sobre: Quantidade de alunos que marcaram sexo como Masculino ou Feminino')

print(enade_df.TP_SEXO.value_counts())

print('\nInformações sobre: Porpoção de alunos que marcaram Masculino ou Feminino em relação ao total de alunos em %')
print(f'{round((enade_df.TP_SEXO.value_counts() / enade_df.shape[0]) * 100, 2)}')


print('\nInformações sobre: Notas Gerais, Notas de Formação Geral e Notas Específicas')
print(enade_df[['NT_GER', 'NT_FG', 'NT_CE']].describe())

print('\nInformações sobre: Notas para cada Região do Brasil')
print(enade_df.groupby('CO_REGIAO_CURSO').agg({
    'NT_GER': 'mean',
    'NT_FG': 'mean',
    'NT_CE': 'mean'
}))

'''
    Executamos funções de agregação específicas para cada coluna determinada dentro de um dicionário
    na função agg()

    Agrupamos todos os dados pela região do brasil para podermos fazer uma comparação entre elas
'''


##############################################################################################################################################################
################################################################## Inicio das tranformações ####################################################


'''
 Colunas que podem sofrer transformações

    - CO_IES: Código da Instituição de ensino    
    - CO_CATEGAD: Categoria admnistratica
    - CO_GRUPO: Categoria do grupo
    - CO_MODALIDADE: Se é presencial(1) ou EAD(0)
    - CO_UF_CURSO 
    - CO_REGIAO_CURSO 
    - NU_IDADE 
    - TP_SEXO
    - NT_GER: Nota geral
    - NT_FG: Nota da formação geral
    - NT_CE: Nota do componente específico 
'''

###### COLUNA DESC_PUBLICA ###################################

# Define se o aluno pertence a uma instituição pública ou privada

print('\nInformações sobre: Quantidade de alunos de instituições públicas e privadas')
enade_df['DESC_PUBLICA'] = ''

enade_df.loc[
    enade_df.CO_CATEGAD.isin([118, 120, 121, 10005, 10006, 10007, 10008, 10009, 17634]),
    'DESC_PUBLICA'
] = 'Privado'

'''
    Passamos o valor "Privado" para a coluna DESC_PUBLICA para todas as linhas que possuem na coluna CO_CATEGAD um dos valores de isin([])
'''

enade_df.loc[
    enade_df.CO_CATEGAD.isin([93, 115, 116, 10001, 10002, 10003]),
    'DESC_PUBLICA'
] = 'Público'

'''
    Passamos o valor "Público" para a coluna DESC_PUBLICA para todas as linhas que possuem na coluna CO_CATEGAD um dos valores de isin([])
'''

print(enade_df.DESC_PUBLICA.value_counts())

print('\nInformações sobre: Porpoção de alunos de instituições públicas e privadas em relação ao total de alunos em %')
print(f'{round((enade_df.DESC_PUBLICA.value_counts() / enade_df.shape[0]) * 100, 2)}')


############################ COLUNA CO_MODALIDADE ###########################
# Alteramos os valores referentes a presencial e EAD na tabela

# Essa é a alteração realizada mas, para concluir a transformção, precisamos atribui-la a coluna 
'''
    Para atribuirmos valores para a coluna, precisamos utilizar a sintaxe de dataframe['nome_da_coluna']
    Para acessarmos uma coluna dentro do dataframe utilizamos a sintaxe de dataframe.nome_da_coluna 
'''

enade_df['CO_MODALIDADE'] = enade_df.CO_MODALIDADE.replace({
    0: 'EAD',
    1: 'Presencial'
})



########################## COLUNA CO_REGIAO_CURSO ############################
'''
    Aqui modificamos o valor da variável original. Essa NÃO é uma boa prática.
    O ideal é seguirmos o método utilizado no exemplo da CO_MODALIDADE
'''

enade_df['CO_REGIAO_CURSO'] = enade_df.CO_REGIAO_CURSO.replace({
    1: 'Norte',
    2: 'Nordeste',
    3: 'Sudeste',
    4: 'Sul',
    5: 'Centro-Oeste'
})


######################### COLUNA QE_I02 - Cor ou raça ################################

# Verificando casos da coluna

print(dict(enade_df.QE_I02.value_counts()))

'''
    Podemos perceber que uma das opções é, na verdade, um espaço vazio
'''

enade_df['DESC_COR'] = enade_df.QE_I02.replace({
    'A': 'Branca',
    'B': 'Preta',
    'C': 'Amarela',
    'D': 'Parda',
    'E': 'Indígena',
    'F': pd.NA,
    ' ': pd.NA 
})

'''
    Utilizamos pd.NA para tranformar os valores faltantes em valores nulos
'''


# Questionamentos

# 1. Nota geral média de alunos da Região Nordeste
print('\nInformações sobre:Nota geral média de alunos da Região Nordeste')
print(enade_df.loc[
    enade_df.CO_REGIAO_CURSO == 'Nordeste',
    'NT_GER'
].mean())

# 2. Qual a média da nota do componente específico dos alunos do Rio Grande do Sul de cursos de Engenharia Elétrica
print('\nInformações sobre: Média da nota de componente específico de alunod do RS do curso de Engenharia Elétrica')
print(enade_df.loc[
    (enade_df.CO_UF_CURSO == 43) &
    (enade_df.CO_GRUPO == 5806),
    'NT_CE'
].mean())

# # 3. Média da nota de componente Geral de alunas(feminino), pardas, de Minas Gerais, em cursos presenciais de Engenharia de Produção

print('\nInformações sobre: Média da nota de componente Geral de alunas(feminino), pardas, de Minas Gerais, em cursos presenciais de Engenharia de Produção')

print(enade_df.loc[
    (enade_df.TP_SEXO == 'F') &
    (enade_df.DESC_COR == 'Parda') &
    (enade_df.CO_UF_CURSO == 31) &
    (enade_df.CO_MODADELIDADE == 'Presencial' ) &
    (enade_df.CO_GRUPO == 6208),
    'NT_FG'
].mean())