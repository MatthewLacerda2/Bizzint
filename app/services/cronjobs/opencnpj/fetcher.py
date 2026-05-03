import asyncio
import httpx
import logging
from datetime import datetime
from typing import List
from .response import OpenCnpjResponse
from ....repositories.company_repository import CompanyRepository
from ....repositories.socio_repository import SocioRepository
from ....utils.envs import OPENCNPJ_DELAY
from ....core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

async def fetch_and_save_cnpjs(cnpj_list: List[str]):
    base_url = "https://api.opencnpj.org"

    async with httpx.AsyncClient() as client:
        for i, cnpj in enumerate(cnpj_list):
            async with AsyncSessionLocal() as db:
                company_repo = CompanyRepository(db)
                socio_repo = SocioRepository(db)
                
                try:
                    logger.info(f"Fetching CNPJ {cnpj} ({i+1}/{len(cnpj_list)})")
                    response = await client.get(f"{base_url}/{cnpj}?dataset=receita", timeout=15.0)
                    
                    if response.status_code == 404:
                        logger.warning(f"CNPJ {cnpj} not found in OpenCNPJ API (404). Skipping.")
                    else:
                        response.raise_for_status()
                        
                        raw_data = response.json()
                        parsed_data = OpenCnpjResponse(**raw_data)
                        
                        # Prepare company data
                        data_inicio = datetime.combine(parsed_data.data_inicio_atividade, datetime.min.time())
                        
                        cap_social = None
                        if parsed_data.capital_social:
                            try:
                                # Handles "1000,00" or "1.000,00" or "1000.00"
                                cleaned_cap = parsed_data.capital_social.replace(".", "").replace(",", ".")
                                cap_social = float(cleaned_cap)
                            except ValueError:
                                logger.warning(f"Could not parse capital_social '{parsed_data.capital_social}' for CNPJ {cnpj}")

                        company_data = {
                            "cnpj": parsed_data.cnpj,
                            "razao_social": parsed_data.razao_social,
                            "nome_fantasia": parsed_data.nome_fantasia,
                            "situacao_cadastral": parsed_data.situacao_cadastral,
                            "data_inicio_atividade": data_inicio,
                            "cnae_principal": parsed_data.cnae_principal,
                            "natureza_juridica": parsed_data.natureza_juridica,
                            "bairro": parsed_data.bairro,
                            "cep": parsed_data.cep,
                            "cidade": parsed_data.cidade,
                            "estado": parsed_data.estado,
                            "email": parsed_data.email,
                            "telefone_1": parsed_data.telefone_1,
                            "telefone_2": parsed_data.telefone_2,
                            "capital_social": cap_social
                        }
                        
                        # Check if company exists
                        company = await company_repo.get_by_cnpj(cnpj)
                        
                        if company:
                            await company_repo.update(company.id, company_data)
                            db_company = company
                        else:
                            db_company = await company_repo.create(company_data)
                        
                        # Sync Partners (Socios)
                        existing_socios = await socio_repo.get_by_company_id(db_company.id)
                        for s in existing_socios:
                            await socio_repo.delete(s.id)
                        
                        for socio_resp in parsed_data.socios:
                            socio_data_entrada = datetime.combine(socio_resp.data_entrada, datetime.min.time())
                            await socio_repo.create({
                                "company_id": db_company.id,
                                "name": socio_resp.name,
                                "cnpj_cpf": socio_resp.cnpj_cpf,
                                "qualificacao": socio_resp.qualificacao,
                                "data_entrada": socio_data_entrada,
                                "identificador": socio_resp.identificador,
                                "faixa_etaria": socio_resp.faixa_etaria
                            })
                        
                        logger.info(f"Successfully processed CNPJ {cnpj}")
                    
                except httpx.HTTPStatusError as e:
                    logger.error(f"API error for CNPJ {cnpj}: {e.response.status_code} - {e.response.text}")
                    await db.rollback()
                except Exception as e:
                    logger.error(f"Unexpected error processing CNPJ {cnpj}: {e}", exc_info=True)
                    await db.rollback()
            
            # Delay between requests
            if i < len(cnpj_list) - 1:
                logger.info(f"Waiting {OPENCNPJ_DELAY} seconds before next request...")
                await asyncio.sleep(OPENCNPJ_DELAY)