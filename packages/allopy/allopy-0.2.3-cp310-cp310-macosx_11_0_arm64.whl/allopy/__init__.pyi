from typing import Any

class AllopyError(Exception): ...

def encode(params: Any, signature: str) -> bytes: ...
def encode_calldata(signature: str, params: tuple[Any, ...]) -> bytes: ...
async def fetch_storage(
    contract: str, slot: bytes, signature: str, block: int, rpc_url: str
) -> Any: ...
async def fetch_storage_map(
    contract: str,
    slot: bytes,
    key: Any,
    key_signature: str,
    value_signature: str,
    block: int,
    rpc_url: str,
) -> Any: ...
