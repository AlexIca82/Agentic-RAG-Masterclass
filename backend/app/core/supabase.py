from supabase import create_client, Client
from app.core.config import get_settings

_settings = get_settings()

supabase: Client = create_client(_settings.supabase_url, _settings.supabase_anon_key)

supabase_admin: Client = create_client(
    _settings.supabase_url, _settings.supabase_service_role_key
)
