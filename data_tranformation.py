# Enade Data Transformation - Aula 3 Módulo 1 Bootcamp IGTI Engenharia de Dados

import pandas as pd
import numpy as np
import os



enade_df = pd.read_csv(
    './../enade_data_extraction/enade2019/microdados_enade_2019/2019/3.DADOS/microdados_enade_2019.txt',
    sep = ';',
    decimal = ','
) 

# Primeiras 5 linhas
# print(enade_df.head())

# Verificando a tipagem dos dados da tabela
# print(dict(enade_df.dtypes))


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
# print('Informações sobre: Dataframe')
# print(enade_df.shape)
# # NT_GER
# print('Informações sobre: Notas Gerais')
# print(enade_df.NT_GER.describe())


# # Contar o número de nulos
# NT_GER_TOTAL_NULLS = enade_df.NT_GER.isnull().sum()
# print('Total de notas gerais nulas: ',NT_GER_TOTAL_NULLS)

# # Porcentagem de nulos em relação ao total de linhas

# print(f'% de notas gerais nulas em relação ao total: \n{round((NT_GER_TOTAL_NULLS / enade_df.shape[0]) * 100, 2)}%')


# # .loc filtra linhas do dataframe por um condição
# # CO_REGIAO_CURSO == 2 representa os alunos do Nordetes
# print('Informações sobre: Nota Geral de alunos da Região Nordeste')
# print(enade_df.loc[
#     enade_df.CO_REGIAO_CURSO == 2
# ].NT_GER.describe())

