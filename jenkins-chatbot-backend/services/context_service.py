import httpx
from typing import Optional
from jenkins_chatbot_backend.config import settings

class ContextService:
    def __init__(self):
        self.base_url = settings.jenkins_url
        self.user = settings.jenkins_user
        self.token = settings.jenkins_token
        self.auth = (self.user, self.token)

    async def get_console_log(self, job_name: str) -> Optional[str]:
        url = f"{self.base_url}/job/{job_name}/lastBuild/consoleText"
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.get(url, auth=self.auth)
                resp.raise_for_status()
                return resp.text
        except Exception:
            return "Failed to fetch console log."

    async def get_job_config(self, job_name: str) -> Optional[str]:
        url = f"{self.base_url}/job/{job_name}/config.xml"
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.get(url, auth=self.auth)
                resp.raise_for_status()
                return resp.text
        except Exception:
            return "Failed to fetch job config."

    async def get_build_status(self, job_name: str) -> Optional[str]:
        url = f"{self.base_url}/job/{job_name}/lastBuild/api/json"
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.get(url, auth=self.auth)
                resp.raise_for_status()
                data = resp.json()
                return data.get("result", "Unknown")
        except Exception:
            return "Failed to fetch build status."
