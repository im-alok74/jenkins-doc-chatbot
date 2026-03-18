from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    ollama_base_url: str = Field("http://localhost:11434", env="OLLAMA_BASE_URL")
    llm_provider: str = Field("openai", env="LLM_PROVIDER")
    jenkins_url: str = Field("http://localhost:8080", env="JENKINS_URL")
    jenkins_user: str = Field("admin", env="JENKINS_USER")
    jenkins_token: str = Field(..., env="JENKINS_TOKEN")
    faiss_index_path: str = Field("data/faiss_index", env="FAISS_INDEX_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
