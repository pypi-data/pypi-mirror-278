class TelefoneInvalidoException(Exception):
    
    def __init__(self, message: str):
        self.message = message


class Telefone:
    
    def __init__(
            self, numero: str, 
            codigo_area: str, 
            codigo_pais: str='55', 
            remover_caracteres_especiais: bool=False) -> None:
        self._codigo_area = codigo_area
        self._codigo_pais = codigo_pais
        self._remover_caracteres_especiais = remover_caracteres_especiais
        self._tamanho_minimo_para_telefone_valido = 8
        self._tamanhos_para_telefone_sem_codigo_pais = [10, 11]
        self._tamanhos_para_telefone_sem_codigo_area = [8, 9]
        self._validar_numero_telefone(numero)
        self.numero = self._obter_numero_tratado(numero)
        
    @property
    def eh_movel(self) -> bool:
        return bool(self.numero[4] == '9')
    
    def _validar_numero_telefone(self, numero: str) -> None:
        self._validar_tipo_numero_telefone(numero)
        self._validar_tamanho_minimo_telefone(numero)

    def _obter_numero_tratado(self, numero: str) -> str:
        numero = self._tratar_caracteres_especiais(numero)
        numero = self._converter_numero_para_padrao_e_164(numero)
        return numero
    
    def _validar_tipo_numero_telefone(self, numero: str) -> None:

        if type(numero) != str:
            raise TelefoneInvalidoException('O numero deve ser do tipo string')
        
    def _validar_tamanho_minimo_telefone(self, numero: str) -> None:
        if len(numero) < self._tamanho_minimo_para_telefone_valido:
            raise TelefoneInvalidoException('Erro de tamanho mínimo!')

    def _converter_numero_para_padrao_e_164(self, numero: str) -> str:
                
        if len(numero) in self._tamanhos_para_telefone_sem_codigo_pais:
            return f'{self._codigo_pais}{numero}'
        
        elif len(numero) in self._tamanhos_para_telefone_sem_codigo_area:
            return f'{self._codigo_pais}{self._codigo_area}{numero}'
        
        return numero
    
    def _tratar_caracteres_especiais(self, numero: str) -> str:
        if self._remover_caracteres_especiais:
            caracteres_especiais = [
                '(',
                ')',
                '-',
                ' ',
                '+'
            ]
            
            for caracter in caracteres_especiais:
                numero = numero.replace(caracter, '')

        return numero