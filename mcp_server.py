# Import required libraries
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pyngrok import ngrok
import nest_asyncio
import requests
import wikipediaapi

# Allow FastAPI
nest_asyncio.apply()

app = FastAPI()

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(user_agent="MCP-Server/1.0 (your-email@example.com)", language="en")

# GitHub API
GITHUB_API_URL = "https://api.github.com"

# Stack Overflow API 
STACKOVERFLOW_API_URL = "https://api.stackexchange.com/2.3/search"

# Request model
class QueryRequest(BaseModel):
    query: str

# Function to fetch Wikipedia summaries
def get_wikipedia_summary(topic):
    # Clean up the topic to make it more Wikipedia-friendly
    cleaned_topic = topic.replace("with", "").strip()

    page = wiki_wiki.page(cleaned_topic)

    if page.exists() and "may refer to" not in page.summary.lower():
        return page.summary[:500]  # Limit to 500 characters
    else:
        return f"Could not find an exact Wikipedia page for '{cleaned_topic}'. Try a different keyword."


# Function to fetch GitHub repositories
def get_github_repos(topic):
    url = f"{GITHUB_API_URL}/search/repositories?q={topic}&sort=stars&order=desc"
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json().get("items", [])[:5]  # Get top 5 results

        # Filter out repos with less than 1000 stars (to remove irrelevant repos)
        filtered_repos = [f"{repo['name']} ({repo['html_url']})" 
                          for repo in repos if repo['stargazers_count'] > 1000]
        
        return filtered_repos if filtered_repos else ["No high-quality GitHub repositories found."]
    
    return ["GitHub API request failed."]

# Function to fetch Stack Overflow answers
def get_stackoverflow_answers(query):
    params = {"order": "desc", "sort": "votes", "intitle": query, "site": "stackoverflow"}
    response = requests.get(STACKOVERFLOW_API_URL, params=params)

    if response.status_code == 200:
        questions = response.json().get("items", [])[:3]  # Get top 3 questions
        if not questions:
            return ["No relevant Stack Overflow discussions found."]
        
        return [f"{q['title']} ({q['link']})" for q in questions]

    return ["Stack Overflow API request failed."]

# MCP Endpoint
@app.post("/mcp")
async def mcp_handler(request: QueryRequest):
    """Handles AI developer queries"""
    user_query = request.query.lower()

    # Extract only the topic from the user's request
    topic = (
        user_query.replace("explain", "")
        .replace("github repos", "")
        .replace("stack overflow", "")
        .replace("with", "")
        .replace("and", "")
        .replace("discussions", "")
        .strip()
    )

    if not topic:
        return {"response": "Please provide a valid tech topic, e.g., 'Explain Python with GitHub repos and Stack Overflow discussions'."}

    # Fetch data from all 3 APIs
    summary = get_wikipedia_summary(topic)
    repos = get_github_repos(topic)
    answers = get_stackoverflow_answers(topic)

    return {
    "response": (
        f"📖 **Wikipedia Summary:**\n{summary}\n\n"
        f"🐙 **GitHub Repositories:**\n- " + "\n- ".join(repos) + "\n\n"
        f"💬 **Stack Overflow Discussions:**\n- " + "\n- ".join(answers)
    )
   }


# Start the server with Ngrok
public_url = ngrok.connect(8000).public_url
print(f"Public URL: {public_url}")

# Run FastAPI
uvicorn.run(app, host="0.0.0.0", port=8000)
