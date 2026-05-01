from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date

class SocioResponse(BaseModel):
    name: str = Field(alias="nome_socio")
    cnpj: str = Field(alias="cnpj_cpf_socio")
    qualificacao: str = Field(alias="qualificacao_socio")
    data_entrada: date = Field(alias="data_entrada_sociedade")
    identificador: str = Field(alias="identificador_socio")
    faixa_etaria: str = Field(alias="faixa_etaria")

    class Config:
        populate_by_name = True

class OpenCnpjResponse(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    situacao_cadastral: str
    data_inicio_atividade: date
    cnae_principal: str
    natureza_juridica: str
    bairro: str
    cep: str
    cidade: str = Field(alias="municipio")
    estado: str = Field(alias="uf")
    email: Optional[str] = None
    telefone_1: Optional[str] = None
    telefone_2: Optional[str] = None
    capital_social: str
    socios: List[SocioResponse] = Field(alias="QSA", default=[])

    @model_validator(mode='before')
    @classmethod
    def handle_phones(cls, data: dict) -> dict:
        telefones = data.get("telefones", [])
        if telefones and len(telefones) >= 1:
            tel1 = telefones[0]
            data["telefone_1"] = f"({tel1.get('ddd')}) {tel1.get('numero')}"
        if telefones and len(telefones) >= 2:
            tel2 = telefones[1]
            data["telefone_2"] = f"({tel2.get('ddd')}) {tel2.get('numero')}"
        return data

    class Config:
        populate_by_name = True