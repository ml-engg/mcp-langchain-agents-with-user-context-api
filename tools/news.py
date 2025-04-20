# Databricks notebook source
import httpx
from langchain.tools import Tool

# COMMAND ----------

# MAGIC %run ../config

# COMMAND ----------

async def news_tool_func(user_query: str) -> str:
    params = {
        "q": f"{user_query} ",
        "engine": "google_news",
        "api_key": serp_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SERP_API_URL, params=params)
        response.raise_for_status()
        news = response.json().get("news_results", [])
    
    if not news:
        return f"No news found for {user_query}"
    return "\n\n".join([f"{n['title']} - {n['link']}" for n in news[:3]])

news_tool = Tool.from_function(
    func=news_tool_func,
    name="NewsTool",
    description="Use this tool to search for recent news about companies. "
                "Input should be a single 'topic' like a company name. Only use when the user asks about news.",
    coroutine= news_tool_func
        
)

