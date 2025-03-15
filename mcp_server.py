# Importing required libraries
import uvicorn                     
from fastapi import FastAPI
from pydantic import BaseModel
from pyngrok import ngrok
import nest_asyncio
import wikipediaapi

# FastAPI
nest_asyncio.apply()            

# Initialize FastAPI
app = FastAPI()                   

# Request model
class QueryRequest(BaseModel):    
    query: str

# Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(user_agent="MCP-Server/1.0 (rishav2207raj@gmail.com)", language="en")

# Function to fetch Wikipedia summaries
def get_wikipedia_summary(topic):
    page = wiki_wiki.page(topic)

    # Check if it's a valid page & not a disambiguation
    if page.exists() and "may refer to" not in page.summary.lower():
        return page.summary[:500]  # Limit to 500 characters
    else:
        return f"Multiple results found for '{topic}'. Please be more specific."

# Root URL - Prevents 404 errors when accessing base URL
@app.get("/")
async def home():
    return {"message": "Welcome to the Wikipedia MCP Server! Use /mcp to interact."}

# MCP Endpoint
@app.post("/mcp")
async def mcp_handler(request: QueryRequest):
    """Handles AI queries to fetch Wikipedia summaries"""
    user_query = request.query.lower()

    if "search wikipedia" in user_query:
        topic = user_query.replace("search wikipedia", "").strip()
        summary = get_wikipedia_summary(topic)
        return {"response": f"Here’s what I found on Wikipedia about {topic}: {summary}"}

    return {"response": "I can search Wikipedia for you. Try: 'Search Wikipedia Python'."}

# Starting the server with Ngrok
public_url = ngrok.connect(8000).public_url
print(f"Public URL: {public_url}")

# Running FastAPI
uvicorn.run(app, host="0.0.0.0", port=8000)
