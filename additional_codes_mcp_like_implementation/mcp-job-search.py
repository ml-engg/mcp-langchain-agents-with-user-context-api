# Databricks notebook source
#!pip install mcp langchain-mcp-adapters fastapi pydantic httpx nest_asyncio uvicorn

# COMMAND ----------

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import httpx
from serpapi.google_search import GoogleSearch

# COMMAND ----------

# MAGIC %run ./secrets

# COMMAND ----------

# MAGIC %run ./config

# COMMAND ----------

SERP_API_URL = ""

# COMMAND ----------

job_app = FastAPI()

class user_job_query(BaseModel):
    user_id: str
    user_query: str

@job_app.post("/job_query")
async def job_query(query: user_job_query):
    params = {
        'q' : query.user_query,
        "engine": "google_jobs",
        "num":20,
        "hl": "en",
        "location": 'Bengaluru, India',
        "gl": "in",
        "api_key": serp_key
        }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(SERP_API_URL, params=params)
        response.raise_for_status()  # raises error if HTTP 4xx/5xx
        results = response.json()

    return {
        "user_id": query.user_id,
        "jobs": results.get("jobs_results", [])
    }

# COMMAND ----------

import uvicorn

# Entry point
if __name__ == "__main__":
    uvicorn.run(job_app, host="0.0.0.0", port=8000)

# COMMAND ----------

