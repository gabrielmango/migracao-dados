import datetime
import uuid
from unicodedata import normalize
from database import DataBase
from database import (
    Pessoa, GeralPessoa, FiliacaoPessoa, Email, Telefone, Endereco, Documento
)

class Consistencia():
    
    def normaliza_coluna(self, texto):
        texto_formatado = self.formatar_texto(texto)
        texto_sem_acentos = normalize('NFKD', texto_formatado).encode('ASCII','ignore').decode('ASCII')
        return texto_sem_acentos.replace(' ', '_').replace('-', '_')
    
    def valida_texto(self, texto):
        texto = texto
        if texto == 'nan' or texto == '' or texto == ' ':
            return True
        return False

    def formatar_texto(self, texto: str):
        return texto.upper().strip()

    def formatar_sexo(self, texto: str):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto)
        
        if texto_formatado == 'M' or texto_formatado == 'MASCULINA':
            return 'MASCULINO'
        elif texto_formatado == 'F' or texto_formatado == 'FEMININA':
            return 'FEMININO'
        return texto_formatado

    def formatar_data_nascimento(self, texto):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto)
        
        texto_formatado = texto_formatado.split('/')
        
        if int(texto_formatado[1]) > 12:
            return f'{texto_formatado[2]}-{texto_formatado[0]}-{texto_formatado[1]}'
        else:
            return f'{texto_formatado[2]}-{texto_formatado[1]}-{texto_formatado[0]}'

    def formatar_etnia(self, texto):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto)
        
        if texto_formatado == 'PARTA' or texto_formatado == 'PARDA':
            return 'PARDO'
        elif texto_formatado == 'NEGRO(A)' or texto_formatado == 'NEGRA' or texto_formatado == 'NEGRO' or texto_formatado == 'PRETA':
            return 'PRETO'
        elif texto_formatado == 'BRANCA':
            return 'BRANCO'
        elif texto_formatado == 'INDÍGENA':
            return 'INDIGENA'
        elif texto_formatado == 'AMARELA':
            return 'AMARELO'
        return texto_formatado

    def formatar_nacionalidade(self, texto):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto)    
        
        if texto_formatado == 'BRASILEIRO' or texto_formatado == 'CONTAGEM':
            return 'BRASILEIRA'
        return texto_formatado

    def formatar_numero_contato(self, texto):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto) 
        
        celular_formatado = texto_formatado.strip().replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('.', '')
            
        if celular_formatado.startswith('0'):
            celular_formatado = celular_formatado[1:]
            
        return celular_formatado  

    def formatar_numero_identificacao(self, texto):
        if self.valida_texto(texto):
            return None
        
        texto_formatado = self.formatar_texto(texto)
        
        numero_final = texto_formatado.strip().replace('.', '').replace('-', '').replace(' ', '').replace('_', '')
        
        return numero_final
    
class InsertPessoa():
    def __init__(self, couuid_1: str, dado: str):
        self._couuid_1 = couuid_1
        self.dado = dado
        self.database = DataBase()
    
    def _cria_dados_insert(self):
        return { 
        'st_ativo': True,
        'dh_criacao': str(datetime.datetime.now()),
        'dh_alteracao': None,
        'tp_operacao': 'CREATE',
        'nu_versao': 1,
        'co_uuid_1': self._couuid_1,
        'co_uuid': str(uuid.uuid4()),
        }
    

    def insert_tabela_pessoas(self, uuid_pessoa: str):
            dados_tabela_pessoa = self._cria_dados_insert()
            dados_tabela_pessoa['no_pessoa'] = self.dado['NOME']
            dados_tabela_pessoa['fl_nome_social_pessoa'] = self.dado['NOME_SOCIAL']
            dados_tabela_pessoa['no_lingua_falada_pessoa'] = self.dado['PASTA']
            dados_tabela_pessoa['co_uuid'] = uuid_pessoa     
            self.database.insert(Pessoa, dados_tabela_pessoa)
    
            
    def insert_tabela_geralpessoa(self, uuid_pessoa: str):
            dados_tabela_geralpessoa = self._cria_dados_insert()
            dados_tabela_geralpessoa['co_uuid_2'] = uuid_pessoa
            dados_tabela_geralpessoa['dt_nascimento_pessoa'] = self.dado['DATA_DE_NASCIMENTO']
            dados_tabela_geralpessoa['no_estado_civil_pessoa'] = self.dado['ESTADO_CIVIL']
            dados_tabela_geralpessoa['no_sexo_pessoa'] = self.dado['SEXO']
            dados_tabela_geralpessoa['no_genero_pessoa'] = self.dado['GENERO']
            dados_tabela_geralpessoa['no_etnia_pessoa'] = self.dado['ETNIA']
            self.database.insert(GeralPessoa, dados_tabela_geralpessoa)


    def insert_tabela_filiacao(self, id_geralpessoa: str, filiacao: int):
            if filiacao == 1:
                dados_tabela_filiacao_1 = self._cria_dados_insert()
                dados_tabela_filiacao_1['co_geral_pessoa'] = id_geralpessoa
                dados_tabela_filiacao_1['ds_nivel_parent_filiac_pessoa'] = 'PRIMEIRO_GRAU'
                dados_tabela_filiacao_1['no_sexo_parent_filiac_pessoa'] = 'FEMININO'
                dados_tabela_filiacao_1['no_filiacao_pessoa'] = self.dado['FILIACAO_1']
                self.database.insert(FiliacaoPessoa, dados_tabela_filiacao_1)
            elif filiacao == 2:
                dados_tabela_filiacao_2 = self._cria_dados_insert()
                dados_tabela_filiacao_2['co_geral_pessoa'] = id_geralpessoa
                dados_tabela_filiacao_2['ds_nivel_parent_filiac_pessoa'] = 'PRIMEIRO_GRAU'
                dados_tabela_filiacao_2['no_sexo_parent_filiac_pessoa'] = 'MASCULINO'
                dados_tabela_filiacao_2['no_filiacao_pessoa'] = self.dado['FILIACAO_2']
                self.database.insert(FiliacaoPessoa, dados_tabela_filiacao_2)
                
    def insert_tabela_email(self, uuid_pessoa: str):
            dados_tabela_email = self._cria_dados_insert()
            dados_tabela_email['co_uuid_2'] = uuid_pessoa
            dados_tabela_email['ds_email'] = self.dado['E_MAIL']
            self.database.insert(Email, dados_tabela_email)

    def insert_tabela_documento(self, uuid_pessoa: str, tipo: str, documento: str):
            dados_tabela_documento = self._cria_dados_insert()
            dados_tabela_documento['co_uuid_2'] = uuid_pessoa
            dados_tabela_documento['tp_documento'] = tipo
            dados_tabela_documento['nu_documento'] = documento
            self.database.insert(Documento, dados_tabela_documento)
            
    def insert_tabela_telefone(self, uuid_pessoa, contato, tipo, principal):
            dados_tabela_telefone = self._cria_dados_insert()
            dados_tabela_telefone['co_uuid_2'] = uuid_pessoa
            dados_tabela_telefone['nu_telefone'] = contato
            dados_tabela_telefone['tp_telefone'] = tipo
            dados_tabela_telefone['fl_telefone_principal'] = principal
            self.database.insert(Telefone, dados_tabela_telefone)
            
    def insert_tabela_endereco(self, uuid_pessoa):
            dados_tabela_endereco = self._cria_dados_insert()
            dados_tabela_endereco['co_uuid_2'] = uuid_pessoa
            dados_tabela_endereco['no_endereco'] = self.dado['TIPO'] + ' ' + self.dado['LOGRADOURO']
            dados_tabela_endereco['nu_endereco'] = self.dado['NUMERO']
            dados_tabela_endereco['no_bairro'] = self.dado['BAIRRO']
            dados_tabela_endereco['nu_cep'] = self.dado['CEP']
            dados_tabela_endereco['ds_complemento_endereco'] = self.dado['COMPLEMENTO']
            dados_tabela_endereco['fl_ender_principal'] = True
            dados_tabela_endereco['fl_endereco_invalido'] = False
            self.database.insert(Endereco, dados_tabela_endereco)
            
    def pessoa_na_base(self):
        if self.database.documento_existente(self.dado['CPF'], 'CPF'):
            return True
        if self.database.documento_existente(self.dado['RG'], 'RG'):
            return True
        
        couuid_pessoa = self.database.consultar_nome(self.dado['NOME'])
        existencia_nascimento = False
        if couuid_pessoa:
            existencia_nascimento = self.database.consultar_nascimento(couuid_pessoa)
        if existencia_nascimento:
            return True
        return False
            
    def executa_insert(self):
        # Insert tabela tb_pessoa
        uuid_pessoa = str(uuid.uuid4())
        self.insert_tabela_pessoas(uuid_pessoa)
        
        # Insert tabela tb_geralpessoa
        self.insert_tabela_geralpessoa(uuid_pessoa)
        
        # Insert tabela tb_filiacaopessoa
        id_geralpessoa = self.database.consultar_id_geralpessoa(str(uuid_pessoa))
        if self.dado['FILIACAO_1']:
            self.insert_tabela_filiacao(id_geralpessoa, 1)
        if self.dado['FILIACAO_2']:
            self.insert_tabela_filiacao(id_geralpessoa, 2)
        
        # Insert tabela tb_email
        if self.dado['E_MAIL']:
            self.insert_tabela_email(uuid_pessoa)
            
        # Insert tabela tb_documento
        if self.dado['CPF']:
            self.insert_tabela_documento(uuid_pessoa, 'CPF', self.dado['CPF'])
        if self.dado['RG']:
            self.insert_tabela_documento(uuid_pessoa, 'IDENTIDADE', self.dado['RG'])
        if self.dado['N_INFOPEN']:
            self.insert_tabela_documento(uuid_pessoa, 'INFOPEN', self.dado['N_INFOPEN'])
        if self.dado['N_PRONTUARIO']:
            self.insert_tabela_documento(uuid_pessoa, 'PRONTUARIO', self.dado['N_PRONTUARIO'])
            
        # Insert tabela tb_telefone
        if self.dado['TELEFONE']:
            self.insert_tabela_telefone(uuid_pessoa, self.dado['TELEFONE'], 'TELEFONE', False)
        if self.dado['CELULAR']:
            self.insert_tabela_telefone(uuid_pessoa, self.dado['CELULAR'], 'CELULAR', True)
            
        # Insert tabela tb_endereco   
        if self.dado['LOGRADOURO']:
            self.insert_tabela_endereco(uuid_pessoa)