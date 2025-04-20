# mcp-langchain-agents-with-user-context-api

1. tool - 
        jobsearch agent 
        news agent  
2. agentic ai tool (langchain) - MCP structure 
        agent determines based on user query which tool to invode 
4. rag to store & retrive user level historical conversation for context 
5. fastapi 
        user management
        concurrency 
        user level context reterival 
 
6. tested concurrency of the rest-api 

note: 
ai tools was used to create codes 
databricks was used as llm were already provided & served as endpoint 
    alternative approach: 
        1. deploy fastapi in AKS instead of long running job clusters -- that is more optimal for hostinng microservie 
        2. creata a custom endpoint in databricks model serving
    
next steps: 
create a approach for evaluation 
        1. evaluate at each process 
        2. overall functional evaluation 
