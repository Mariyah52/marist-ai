from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Marist"
    environment: str = "development"
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite:///./marist.db"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-5-5"
    anthropic_base_url: str = "https://api.anthropic.com"
    ollama_url: str = "http://127.0.0.1:11434/api/chat"
    ollama_model: str = "qwen2.5:3b"
    allowed_origins: str = "https://www.imadi.tech,https://imadi.tech,https://maria-aziz-portfolio.onrender.com"
    chat_rate_limit: int = 20
    chat_rate_window_seconds: int = 600
    whatsapp_app_secret: str = ""
    whatsapp_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_verify_token: str = "change-this"
    whatsapp_graph_version: str = "v23.0"
    marist_admin_number: str = ""
    admin_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
