from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
from typing import Optional

from app.database import get_clientes_collection
from app.models.cliente import ClienteCreate, ClienteUpdate, ClienteOut, StatusResponse

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])


def cliente_para_saida(doc: dict) -> dict:
    """Converte um documento do MongoDB (com _id ObjectId) para o formato de saída da API."""
    doc["_id"] = str(doc["_id"])
    return doc


# ---------------------------------------------------------------------------
# REQUISITO 2 — Webservice com envio de dados/comando e recebimento de status
# ---------------------------------------------------------------------------
@router.post("", response_model=StatusResponse, status_code=201)
async def criar_cliente(cliente: ClienteCreate):
    """Cadastra um novo cliente e retorna status de sucesso ou erro."""
    colecao = get_clientes_collection()

    existente = await colecao.find_one({"email": cliente.email})
    if existente:
        raise HTTPException(status_code=409, detail="Já existe um cliente com este e-mail.")

    agora = datetime.now(timezone.utc)
    novo_cliente = cliente.model_dump()
    novo_cliente["criado_em"] = agora
    novo_cliente["atualizado_em"] = agora

    resultado = await colecao.insert_one(novo_cliente)

    return StatusResponse(
        sucesso=True,
        mensagem="Cliente cadastrado com sucesso.",
        dados={"id": str(resultado.inserted_id)}
    )


@router.put("/{cliente_id}", response_model=StatusResponse)
async def atualizar_cliente(cliente_id: str, cliente: ClienteUpdate):
    """Atualiza dados de um cliente existente e retorna status da operação."""
    colecao = get_clientes_collection()

    try:
        oid = ObjectId(cliente_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de cliente inválido.")

    dados_atualizados = {k: v for k, v in cliente.model_dump().items() if v is not None}
    if not dados_atualizados:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    dados_atualizados["atualizado_em"] = datetime.now(timezone.utc)

    resultado = await colecao.update_one({"_id": oid}, {"$set": dados_atualizados})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    return StatusResponse(sucesso=True, mensagem="Cliente atualizado com sucesso.")


@router.delete("/{cliente_id}", response_model=StatusResponse)
async def remover_cliente(cliente_id: str):
    """Remove um cliente e retorna status da operação."""
    colecao = get_clientes_collection()

    try:
        oid = ObjectId(cliente_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de cliente inválido.")

    resultado = await colecao.delete_one({"_id": oid})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    return StatusResponse(sucesso=True, mensagem="Cliente removido com sucesso.")


# ---------------------------------------------------------------------------
# REQUISITO 3 — Webservice com busca de informação mediante uma chave
# ---------------------------------------------------------------------------
@router.get("/{cliente_id}", response_model=ClienteOut)
async def buscar_cliente_por_id(cliente_id: str):
    """Busca um cliente específico pela sua chave única (ID)."""
    colecao = get_clientes_collection()

    try:
        oid = ObjectId(cliente_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de cliente inválido.")

    cliente = await colecao.find_one({"_id": oid})

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    return cliente_para_saida(cliente)


# ---------------------------------------------------------------------------
# REQUISITO 5 — Webservice para trazer lista de itens mediante um filtro
# ---------------------------------------------------------------------------
@router.get("", response_model=list[ClienteOut])
async def listar_clientes(
    nome: Optional[str] = Query(None, description="Filtra por nome (busca parcial, case-insensitive)"),
    cidade: Optional[str] = Query(None, description="Filtra por cidade exata"),
    estado: Optional[str] = Query(None, description="Filtra por sigla do estado, ex: SC"),
    ativo: Optional[bool] = Query(None, description="Filtra por status ativo/inativo"),
):
    """Lista clientes cadastrados, podendo aplicar filtros opcionais."""
    colecao = get_clientes_collection()

    filtro = {}
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}
    if cidade:
        filtro["cidade"] = cidade
    if estado:
        filtro["estado"] = estado.upper()
    if ativo is not None:
        filtro["ativo"] = ativo

    clientes = []
    async for doc in colecao.find(filtro).sort("criado_em", -1):
        clientes.append(cliente_para_saida(doc))

    return clientes
