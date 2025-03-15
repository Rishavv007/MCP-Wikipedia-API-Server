# MCP-Wikipedia-API-Server
A FastAPI-MCP server that fetches Wikipedia summaries for AI assistants, deployed using Google Colab and Ngrok.

# 📚 MCP Wikipedia API Server

This project implements a **Model Context Protocol (MCP) server** using **FastAPI** to allow AI assistants to fetch Wikipedia summaries. The server is deployed on **Google Colab** and exposed via **Ngrok**.

---

## Features
Fetches Wikipedia summaries based on user queries  
Runs as an **MCP-compatible server** for AI interactions  
Uses **FastAPI** and **Wikipedia API**  
Works with **Google Colab** + **Ngrok** for quick deployment  

---

## How to Run in Google Colab

### 1️⃣ Install Required Dependencies  
Run this command in a Colab cell:
```sh
!pip install fastapi uvicorn pyngrok requests wikipedia-api nest_asyncio
