from supabase import create_client
from supabase.lib.client_options import ClientOptions

from supamodel.config import settings

client = create_client(
    supabase_url=settings.supabase_url,
    supabase_key=settings.supabase_key,
    options=ClientOptions(postgrest_client_timeout=60),
)
