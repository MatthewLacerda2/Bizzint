import re
from typing import List
from pydantic import BaseModel, field_validator, ValidationError

class CNPJValidator(BaseModel):
    cnpj: str

    @field_validator('cnpj')
    @classmethod
    def validate_cnpj_math(cls, v: str) -> str:
        # Remove qualquer caractere que não seja número
        numbers = [int(digit) for digit in re.sub(r'\D', '', v)]

        # Valida se tem 14 dígitos e se não é uma sequência repetida (ex: 111...)
        if len(numbers) != 14 or len(set(numbers)) == 1:
            raise ValueError('CNPJ Inválido')

        # Cálculo dos Dígitos Verificadores
        def calculate_digit(digits, weights):
            sum_digits = sum(d * w for d, w in zip(digits, weights))
            result = 11 - (sum_digits % 11)
            return result if result < 10 else 0

        # Pesos para o primeiro e segundo dígito
        weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # Valida o primeiro dígito
        if numbers[12] != calculate_digit(numbers[:12], weights_1):
            raise ValueError('CNPJ Inválido')

        # Valida o segundo dígito
        if numbers[13] != calculate_digit(numbers[:13], weights_2):
            raise ValueError('CNPJ Inválido')

        return v

def validate_cnpj(v: str) -> str:
    """
    Validates CNPJ format and check digits.
    Returns the cleaned CNPJ (digits only) if valid.
    Raises ValueError if invalid.
    """
    # Remove any non-digit characters
    cleaned = re.sub(r'\D', '', v)
    
    if len(cleaned) != 14 or len(set(cleaned)) == 1:
        raise ValueError('CNPJ Inválido')

    numbers = [int(digit) for digit in cleaned]

    # Check digit calculation
    def calculate_digit(digits, weights):
        sum_digits = sum(d * w for d, w in zip(digits, weights))
        result = 11 - (sum_digits % 11)
        return result if result < 10 else 0

    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    if numbers[12] != calculate_digit(numbers[:12], weights_1):
        raise ValueError('CNPJ Inválido')

    if numbers[13] != calculate_digit(numbers[:13], weights_2):
        raise ValueError('CNPJ Inválido')

    return cleaned

def filter_valid_cnpjs(cnpj_list: List[str]) -> List[str]:
    """Filters a list of CNPJs, returning only the mathematically valid ones."""
    valid_ones = []
    for item in cnpj_list:
        try:
            valid_ones.append(validate_cnpj(item))
        except ValueError:
            continue
    return valid_ones