from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Marist"
    environment: str = "development"
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite:///./marist.db"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5"
    whatsapp_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_verify_token: str = "change-this"
    whatsapp_graph_version: str = "v23.0"
    marist_admin_number: str = ""
    admin_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
