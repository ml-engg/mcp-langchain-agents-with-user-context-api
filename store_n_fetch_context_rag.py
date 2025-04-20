# Databricks notebook source
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

# MAGIC %run ./config

# COMMAND ----------

def get_or_create_tenant_for_user(user_id: str):
    # Initialize AdminClient once (singleton pattern recommended)
    adminClient = AdminClient(Settings(
        is_persistent=True,
        persist_directory=""  # Persistent path in Databricks
        #multitenant = True
    ))


    tenant_id = f"tenant_user_{user_id}"
    database_id = DEFAULT_DATABASE

    try:
        adminClient.get_tenant(tenant_id)
    except Exception:
        adminClient.create_tenant(tenant_id)
        #adminClient.create_database(DEFAULT_DATABASE, tenant_id)
    
    # Create database if missing
    try:
        adminClient.get_database(database_id, tenant_id)
    except Exception:
        adminClient.create_database(database_id, tenant_id)

    return tenant_id, DEFAULT_DATABASE

def store_message(user_id: str, message: str, response: str):
    # Get or create tenant and database for the user
    tenant, database = get_or_create_tenant_for_user(user_id)


    # Initialize tenant-scoped client
    client = PersistentClient(
        path="",
        tenant=tenant,
        database=database
    )

    # Get or create the user-specific collection
    collection_name = "user_contexts"
    collection = client.get_or_create_collection(collection_name)

    # Generate unique doc ID
    doc_id = str(uuid.uuid4())

    # Create a Document with metadata
    doc = Document(
        page_content=message,
        metadata={
            "user_id": user_id,
            "response": response,
            "id": doc_id
        }
    )

    # Add the document to the collection
    collection.add(
        documents=[doc.page_content],
        metadatas=[doc.metadata],
        ids=[doc_id]
    )

    # Perform similarity search for this user (optional, adjust query accordingly)
    try:
        results = collection.query(
            query_texts=[message],  # Empty query or customize as needed
            n_results=100,
            where={"user_id": user_id}  # Filter by user_id to isolate user data
        )
    except Exception as e:
        print(f"Similarity search failed: {e}")
        results = []

    return results

def get_recent_context(user_id: str, query: str, k: int = 10) -> str:
    # Get or create tenant and database for the user
    tenant, database = get_or_create_tenant_for_user(user_id)

    # Initialize tenant-scoped client
    client = PersistentClient(
        path="",
        tenant=tenant,
        database=database
    )

    collection_name = "user_contexts"
    collection = client.get_or_create_collection(collection_name)


    try:
        # Query the collection with similarity search filtered by user_id metadata
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where={"user_id": user_id}
        )
        # Extract documents' content from results
        documents = results.get("documents", [[]])[0]  # results["documents"] is a list of lists
        return "\n".join(documents) if documents else ""
    except Exception as e:
        print(f"[INFO] Similarity search error for {user_id} → {e}")
        return ""

