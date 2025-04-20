# Databricks notebook source
# MAGIC %md
# MAGIC ####### secrets

# COMMAND ----------

from langchain.vectorstores import Chroma
import os
from databricks_langchain import DatabricksEmbeddings
from langchain.schema import Document
import uuid
from chromadb.api.client import Client
import chromadb
from chromadb import DEFAULT_DATABASE, AdminClient, PersistentClient, Settings
from langchain.schema import Document

# COMMAND ----------

serp_key = ''
job_role = ""
SERP_API_URL = ""
VECTORSTORE_PATH = ''

# Initialize AdminClient once (singleton pattern recommended)
adminClient = AdminClient(Settings(
    is_persistent=True,
    persist_directory=""  # Persistent path in Databricks
    #multitenant = True
))


# COMMAND ----------

dbutils.fs.mkdirs(VECTORSTORE_PATH)

# COMMAND ----------

