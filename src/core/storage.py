import uuid
from supabase import create_client, Client
from src.core.config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def upload_imagem(file_bytes: bytes, content_type: str, pasta: str = "projetos") -> str:
    """
    Faz upload de uma imagem para o Supabase Storage.
    Retorna a URL pública do arquivo.
    """
    extensao = content_type.split("/")[-1]  # ex: image/jpeg → jpeg
    nome_arquivo = f"{pasta}/{uuid.uuid4()}.{extensao}"

    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=nome_arquivo,
        file=file_bytes,
        file_options={"content-type": content_type, "upsert": True}
    )

    url_publica = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(nome_arquivo)
    return url_publica


def deletar_imagem(url: str) -> None:
    """
    Remove uma imagem do Supabase Storage com base na URL pública.
    """
    # Extrai o path relativo da URL completa
    # Ex: https://xxx.supabase.co/storage/v1/object/public/projetos/projetos/uuid.jpg
    partes = url.split(f"/object/public/{settings.SUPABASE_BUCKET}/")
    if len(partes) < 2:
        return
    path = partes[1]
    supabase.storage.from_(settings.SUPABASE_BUCKET).remove([path])