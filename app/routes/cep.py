from fastapi import APIRouter
from app.services.viacep_service import consultar_cep

router = APIRouter(prefix="/api/v1/cep", tags=["CEP (Webservice Externo)"])


# ---------------------------------------------------------------------------
# REQUISITO 4 — Uso de um webservice de terceiro (ViaCEP)
# ---------------------------------------------------------------------------
@router.get("/{cep}")
async def buscar_endereco_por_cep(cep: str):
    """
    Consulta o webservice de terceiro ViaCEP (https://viacep.com.br) e
    retorna o endereço completo correspondente ao CEP informado.

    Exemplo: GET /api/v1/cep/01310-100
    """
    endereco = await consultar_cep(cep)
    return endereco
