import httpx
from fastapi import HTTPException

VIACEP_BASE_URL = "https://viacep.com.br/ws"


async def consultar_cep(cep: str) -> dict:
    """
    Consulta o webservice de terceiro ViaCEP (https://viacep.com.br) para
    obter o endereço completo a partir de um CEP.

    Requisito 4 do trabalho: uso de um webservice de terceiro.
    """
    cep_limpo = cep.replace("-", "").replace(".", "").strip()

    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        raise HTTPException(
            status_code=400,
            detail="CEP inválido. Use o formato 00000000 ou 00000-000."
        )

    url = f"{VIACEP_BASE_URL}/{cep_limpo}/json/"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resposta = await client.get(url)
        except httpx.RequestError:
            raise HTTPException(
                status_code=503,
                detail="Não foi possível contatar o serviço ViaCEP. Tente novamente mais tarde."
            )

    if resposta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar o serviço externo ViaCEP."
        )

    dados = resposta.json()

    # O ViaCEP retorna {"erro": true} quando o CEP não existe
    if dados.get("erro"):
        raise HTTPException(status_code=404, detail=f"CEP {cep} não encontrado.")

    return {
        "cep": dados.get("cep"),
        "logradouro": dados.get("logradouro"),
        "bairro": dados.get("bairro"),
        "cidade": dados.get("localidade"),
        "estado": dados.get("uf"),
    }
