# Databricks notebook source
#!pip install databricks_langchain

# COMMAND ----------

from databricks_langchain import ChatDatabricks
from langchain.agents import initialize_agent

# COMMAND ----------

DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

# COMMAND ----------

from databricks_langchain import ChatDatabricks
from langchain.agents import initialize_agent, Tool
import httpx


def job_search_tool_func(user_id: str, user_query: str):
    response = httpx.post(
        "",
        headers={"Authorization": ""},
        json={"user_id": user_id, "user_query": user_query}
    )
    response.raise_for_status()
    return response.text

def agent_factory():
    # 🧱 Build LLM per request
    llm = ChatDatabricks(
        endpoint="databricks-meta-llama-3-1-8b-instruct",
        temperature=0.3,
        max_tokens=1256
    )

    # 🛠️ Build tool per request
    job_tool = Tool.from_function(
        name="JobSearchTool",
        func=lambda x: job_search_tool_func(**eval(x)),
        description="Tool to search and return jobs. Input: dict with 'user_id' and 'user_query'."
    )

    # ⚙️ Build agent per user
    agent = initialize_agent(
        tools=[job_tool],
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AgentQuery(BaseModel):
    user_id: str
    user_query: str

@app.post("/mcp_agent")
async def mcp_agent(query: AgentQuery):
    print(query)
    try:
        input_str = str({"user_id": query.user_id, "user_query": query.user_query})
        print(input_str)
        agent = agent_factory()
        result = await agent.ainvoke({"input": input_str})
        content = result.content if hasattr(result, "content") else str(result)
        return {"result": content}
    except Exception as e:
        print(f"[ERROR] {query.user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# COMMAND ----------

import uvicorn
import nest_asyncio

# Apply the nest_asyncio patch
nest_asyncio.apply()

# Entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

