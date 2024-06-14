import pandas as pd
import numpy as np

def ahp_positivos(tabela):
    table = []
    for i in tabela.columns:
        a = tabela[i] / tabela[i].sum()
        table.append(a)
    table = pd.DataFrame(table).T
    return table

def numeros_negativos(tabela):
    table = []
    for i in tabela.columns:
        a = 1 / tabela[i]
        table.append(a)
    table = pd.DataFrame(table).T
    tab_final = []
    for i in table.columns:
        b = table[i] / table[i].sum()
        tab_final.append(b)
    tab_final = pd.DataFrame(tab_final).T
    return tab_final

def matriz_de_decisao(tabela, fator, colunas_para_calculo):
    table = []
    for i in colunas_para_calculo:
        a = tabela[i] * fator[i][0]
        table.append(a)
    table = pd.DataFrame(table).T
    return table

def calcular_ahp_gaussiano(positivos, negativos):
    # Converter colunas de positivos para numéricas
    positivos = positivos.apply(pd.to_numeric, errors='coerce')
    positivos = ahp_positivos(positivos)

    # Converter colunas de negativos para numéricas
    negativos = negativos.apply(pd.to_numeric, errors='coerce')
    negativos = numeros_negativos(negativos)

    tabela_ahp = pd.concat([positivos, negativos], axis=1)

    medias = pd.DataFrame(tabela_ahp.mean(), columns=['media'])
    desvio = pd.DataFrame(tabela_ahp.std(), columns=['desvio'])
    fator_ahp = pd.concat([medias, desvio], axis=1)
    fator_ahp['desvio'] = fator_ahp['desvio'].fillna(np.mean(fator_ahp['desvio']))
    fator_ahp['desvio/media'] = fator_ahp['desvio'] / fator_ahp['media']
    fator_ahp['fator_gaussiano'] = fator_ahp['desvio/media'] / fator_ahp['desvio/media'].sum()
    fator = fator_ahp['fator_gaussiano']
    fator = pd.DataFrame(fator).T
    colunas_para_calculo = fator.columns

    resultado_ahp = matriz_de_decisao(tabela_ahp, fator, colunas_para_calculo)

    soma = resultado_ahp.sum(axis=1)
    soma = pd.DataFrame(soma, columns=['soma'])
    soma = soma.sort_values(by='soma', ascending=False)
    soma = soma.reset_index(drop=True)

    return soma
