# Databricks notebook source
from databricks_langchain import ChatDatabricks
from langchain.agents import initialize_agent

# COMMAND ----------

# MAGIC %run ./tools/job_search_tool

# COMMAND ----------

# MAGIC %run ./tools/news

# COMMAND ----------

def agent_factory():
    llm = ChatDatabricks(
        endpoint="databricks-meta-llama-3-1-8b-instruct",
        temperature=0.1,
        max_tokens=1256
    )
    return initialize_agent(
        tools=[job_tool, news_tool],
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        max_iterations=10,             
        max_execution_time=60   
    )


# COMMAND ----------

