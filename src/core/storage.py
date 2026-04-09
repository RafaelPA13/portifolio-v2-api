import uuid
from typing import Optional
import httpx
from core.config import settings

# Base URL do Storage
# A API de storage do Supabase fica em: {SUPABASE_URL}/storage/v1
STORAGE_BASE_URL = f"{settings.SUPABASE_URL}/storage/v1"

def _auth_headers() -> dict:
    """
    Headers de autenticação usando a secret key do projeto.
    """
    return {
        "apikey": settings.SUPABASE_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_KEY}",
    }

def upload_imagem(file_bytes: bytes, content_type: str, pasta: str = "projetos") -> str:
    """
    Faz upload de uma imagem para o Supabase Storage via HTTP.
    Retorna a URL pública do arquivo.
    """
    extensao = content_type.split("/")[-1] or "bin"
    nome_arquivo = f"{pasta}/{uuid.uuid4()}.{extensao}"

    url = f"{STORAGE_BASE_URL}/object/{settings.SUPABASE_BUCKET}/{nome_arquivo}"

    headers = _auth_headers() | {
        "Content-Type": content_type,
    }

    # upload (upsert = true para sobrescrever se já existir)
    params = {"upsert": "true"}

    resp = httpx.post(url, headers=headers, params=params, content=file_bytes)
    if resp.status_code not in (200, 201):
        # Se quiser, loga resp.text para debug
        raise RuntimeError(f"Erro ao fazer upload no Supabase Storage: {resp.status_code} - {resp.text}")

    # URL pública segue o padrão:
    # {SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{caminho}
    public_url = f"{STORAGE_BASE_URL}/object/public/{settings.SUPABASE_BUCKET}/{nome_arquivo}"
    return public_url

def deletar_imagem(url_publica: str) -> None:
    """
    Remove uma imagem do Supabase Storage com base na URL pública.
    """
    # Espera formato:
    # https://<project>.supabase.co/storage/v1/object/public/<bucket>/<path>
    prefixo = f"{STORAGE_BASE_URL}/object/public/{settings.SUPABASE_BUCKET}/"
    if not url_publica.startswith(prefixo):
        # URL não é do padrão esperado, não vamos apagar nada
        return

    caminho_relativo = url_publica[len(prefixo):]

    url = f"{STORAGE_BASE_URL}/object/{settings.SUPABASE_BUCKET}/{caminho_relativo}"

    headers = _auth_headers()

    resp = httpx.delete(url, headers=headers)
    # 200/204 ok; se der erro, você pode logar mas não precisa quebrar a API
    if resp.status_code not in (200, 204):
        # opcional: logar erro
        pass
    
def upload_pdf(file_bytes: bytes, nome_arquivo: str) -> str:
    """
    Faz upload de um PDF para o bucket de currículos no Supabase Storage.
    Sempre sobrescreve o arquivo anterior de mesmo nome (upsert).
    Retorna a URL pública do arquivo.
    """
    caminho = f"curriculo/{nome_arquivo}"

    url = f"{STORAGE_BASE_URL}/object/{settings.SUPABASE_BUCKET_CURRICULO}/{caminho}"

    headers = _auth_headers() | {
        "Content-Type": "application/pdf",
    }

    resp = httpx.post(url, headers=headers, params={"upsert": "true"}, content=file_bytes)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Erro ao fazer upload do currículo: {resp.status_code} - {resp.text}")

    public_url = f"{STORAGE_BASE_URL}/object/public/{settings.SUPABASE_BUCKET_CURRICULO}/{caminho}"
    return public_url


def deletar_pdf(url_publica: str) -> None:
    """
    Remove um PDF do bucket de currículos no Supabase Storage.
    """
    prefixo = f"{STORAGE_BASE_URL}/object/public/{settings.SUPABASE_BUCKET_CURRICULO}/"
    if not url_publica.startswith(prefixo):
        return

    caminho_relativo = url_publica[len(prefixo):]
    url = f"{STORAGE_BASE_URL}/object/{settings.SUPABASE_BUCKET_CURRICULO}/{caminho_relativo}"

    resp = httpx.delete(url, headers=_auth_headers())
    if resp.status_code not in (200, 204):
        pass