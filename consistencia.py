from unicodedata import normalize

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