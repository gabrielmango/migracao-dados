import pandas as pd
from database import DataBase
from consistencia import Consistencia, InsertPessoa

dados = pd.read_csv('Migração.csv')
print('Dados carregados da planilha.')

dados_list = []
pessoas_nao_cadastradas = []

couuid_1 = 'python-gabriel'

consistencia = Consistencia()
database = DataBase()

database.reset_db()
print('Tabela criadas no banco de dados.')

for number in range(len(dados)):
    
    dado = dict(dados.iloc[number])
    
    dado_formatado = {}
    
    for key, value in dado.items():
        
        texto = str(value)
        
        if key == 'Sexo':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_sexo(texto)
        elif key == 'Data de Nascimento ':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_data_nascimento(texto)
        elif key == 'Etnia':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_etnia(texto)
        elif key == 'Nacionalidade':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_nacionalidade(texto)
        elif key == 'Celular' or key == 'Telefone':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_numero_contato(texto)
        elif key == 'CPF' or key == 'RG' or key == 'N° INFOPEN' or key == 'N° PRONTUÁRIO' or key == 'CEP':
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_numero_identificacao(texto)
        elif consistencia.valida_texto(texto):
            dado_formatado[consistencia.normaliza_coluna(key)] = None
        else:
            dado_formatado[consistencia.normaliza_coluna(key)] = consistencia.formatar_texto(texto)
    
    dados_list.append(dado_formatado)
    
print('Dados preprocessados.')

# Pessoas com CPF e com RG
for dado in dados_list:
    if dado['CPF'] and len(dado['CPF']) == 10:
        dado['CPF'] = '0' + dado['CPF']

for dado in dados_list:
    pessoa = InsertPessoa(couuid_1, dado)
    
    if pessoa.pessoa_na_base():
        print(f'{dado["NOME"]} já se encontra na base de dados')
        pessoas_nao_cadastradas.append(dado)

    if dado['CPF'] and (len(dado['CPF']) < 11 or len(dado['CPF']) > 12):
        dado['CPF'] = None
    
    pessoa.executa_insert()

print('Dados carregados no banco de dados.')
print(pessoas_nao_cadastradas)