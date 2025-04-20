# Databricks notebook source
import httpx
from langchain.tools import Tool

# COMMAND ----------

# MAGIC %run ../config

# COMMAND ----------

async def job_search_tool_func(user_query: str) -> str:
    params = {
        "q": user_query,
        "engine": "google_jobs",
        "num": 10,
        "hl": "en",
        "location": "",
        "gl": "in",
        "api_key": serp_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SERP_API_URL, params=params)
        response.raise_for_status()
        jobs = response.json().get("jobs_results", [])
    
    if not jobs:
        return f"No jobs found for {user_query}"
    return "\n\n".join([f"{j['title']} at {j.get('company_name', '')}" for j in jobs[:3]])

job_tool = Tool.from_function(
    func=job_search_tool_func,
    name="JobSearchTool",
    description="Use this tool to search for job listings by role, skills, or location. "
                "Input should include 'user_query'. Only use when the user is looking for job openings.",
    coroutine=job_search_tool_func
)


