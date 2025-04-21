# mcp-langchain-agents-with-user-context-api

1. tool
   
        jobsearch agent 
        news agent  
3. agentic ai tool (langchain) - MCP structure
   
        agent determines based on user query which tool to invode 
5. rag to store & retrive user level historical conversation for context 
6. fastapi
   
        user management
        concurrency 
        user level context reterival 
 
8. tested concurrency of the rest-api
9. Note MCP is not implemented here from mcp package, but under folder "additional_codes_mcp_like_implementation", a fast api server is created mcp_job_search and the same is called in code llm_microservice. This is same concept as MCP 

note: 

    ai tools were leveraged and used as assistant to create codes in this repo 
    databricks was used as llm were already provided & served as endpoint 
    alternative approach: 
        1. deploy fastapi in AKS instead of long running job clusters -- that is more optimal for hosting microservice 
        2. creata a custom endpoint in databricks model serving
    
next steps: 

    create a approach for evaluation 
        1. evaluate at each process 
        2. overall functional evaluation 
