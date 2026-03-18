import os
import httpx
from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.llms import GoogleGenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from jenkins_chatbot_backend.config import settings

JENKINS_SYSTEM_PROMPT = (
    "You are an expert Jenkins CI/CD assistant. You help developers with pipeline creation, build failure debugging, plugin selection, and Jenkins configuration. "
    "Always provide specific, actionable answers. When suggesting Jenkinsfile code, ensure it is valid declarative pipeline syntax. "
    "If unsure, acknowledge uncertainty rather than hallucinating."
)

class LLMService:
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.openai_api_key = settings.openai_api_key
        self.gemini_api_key = settings.gemini_api_key
        self.ollama_base_url = settings.ollama_base_url

    async def get_response(self, query: str, context: Optional[Dict[str, Any]], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": JENKINS_SYSTEM_PROMPT}
        ]
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items() if v)
            messages.append({"role": "system", "content": f"Jenkins context:\n{context_str}"})
        for turn in history:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": query})

        if self.provider == "openai":
            return await self._openai_chat(messages)
        elif self.provider == "gemini":
            return await self._gemini_chat(messages)
        elif self.provider == "ollama":
            return await self._ollama_chat(messages)
        else:
            return {"response": "LLM provider not supported.", "sources": [], "confidence": 0.0}

    async def _openai_chat(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            chat = ChatOpenAI(api_key=self.openai_api_key, model="gpt-4o", temperature=0.2)
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))
            response = await chat.apredict_messages(lc_messages)
            return {"response": response.content, "sources": [], "confidence": 0.95}
        except Exception as e:
            return {"response": f"OpenAI error: {str(e)}", "sources": [], "confidence": 0.0}

    async def _gemini_chat(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            chat = GoogleGenAI(api_key=self.gemini_api_key, model="gemini-pro", temperature=0.2)
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))
            response = await chat.apredict_messages(lc_messages)
            return {"response": response.content, "sources": [], "confidence": 0.90}
        except Exception as e:
            return {"response": f"Gemini error: {str(e)}", "sources": [], "confidence": 0.0}

    async def _ollama_chat(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            prompt = "\n".join([msg["content"] for msg in messages])
            ollama = Ollama(base_url=self.ollama_base_url, model="llama2", temperature=0.2)
            response = await ollama.apredict(prompt)
            return {"response": response, "sources": [], "confidence": 0.80}
        except Exception as e:
            return {"response": f"Ollama error: {str(e)}", "sources": [], "confidence": 0.0}
