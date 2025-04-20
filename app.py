# Databricks notebook source
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import traceback

# COMMAND ----------

# MAGIC %run ./agent_factory

# COMMAND ----------

# MAGIC %run ./store_n_fetch_context_rag

# COMMAND ----------

app = FastAPI()

class UserPrompt(BaseModel):
    user_id: str
    query: str

@app.post("/mcp_agent")
async def mcp_agent(prompt: UserPrompt):
    try:
        get_or_create_tenant_for_user(prompt.user_id)

        #modify 
        try:
            context = get_recent_context(prompt.user_id, prompt.query)
        except Exception as e:
            context = ""
            print("Error getting context:\n", traceback.format_exc())

        
        full_prompt = (
            f"Chat history:\n{context}\n\n"
            f"User ({prompt.user_id}) asks: {prompt.query}\n"
            f"Use only JobSearchTool for jobs.\n"
            f"Use only NewsTool for News.\n"
            f"Assistant:"
        )
    
        agent = agent_factory()
        result = await agent.ainvoke({"input": full_prompt})
        content = getattr(result, "content", str(result))
        try:
            store_message(prompt.user_id, prompt.query, content)
        except Exception as e:
            print("Error getting context:\n", traceback.format_exc())
                  
        return {"result": content}
    except Exception as e:
        print("MCP Agent Error:\n", traceback.format_exc())  # Full traceback
        raise HTTPException(status_code=500, detail=str(e))



# COMMAND ----------

import nest_asyncio
import uvicorn

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)

# COMMAND ----------

