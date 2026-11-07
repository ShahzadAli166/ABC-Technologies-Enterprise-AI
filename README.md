
# ABC Technologies Enterprise AI Assistant

A publicly deployed Enterprise AI application demonstrating company-policy question answering, customer personalization, and business order calculations.

## Live Application

**Dashboard:**  
https://abc-technologies-enterprise-ai-by-shahzad-panhwar.streamlit.app

**Cloudflare API Health:**  
https://abc-technologies-enterprise-aii.panhwarshahzadali91.workers.dev/health

## Application Features

- Enterprise AI dashboard using Streamlit
- AI-powered company-policy assistant
- Customer-specific information retrieval
- Company knowledge retrieval using Cloudflare D1
- AI answer generation using Cloudflare Workers AI
- Automated order-total calculation
- API authentication and request validation

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| API Gateway | Cloudflare Workers |
| AI Model | GLM-4.7-Flash |
| Database | Cloudflare D1 |
| AI Inference | Cloudflare Workers AI |
| Backend Language | JavaScript |
| Frontend Language | Python |
| Source Control | GitHub |

## Example Test Results

| Test | Verified Result |
|---|---|
| Refund deadline | 7 calendar days |
| Order calculation | 8 × 350 = 2,800 PKR |
| Unauthorized API request | HTTP 401 |
| Unknown customer | HTTP 404 |
| Invalid order quantity | HTTP 400 |

## Project Documentation

- [System Architecture](ABC_Technologies_Project_Documentation/ABC_Technologies_GitHub_Repository/docs/ARCHITECTURE.md)
- [Project Case Study](ABC_Technologies_Project_Documentation/ABC_Technologies_GitHub_Repository/docs/CASE_STUDY.md)
- [Additional Documentation](ABC_Technologies_Project_Documentation/README.md)

## Architecture Overview

Customer
   |
   v
Streamlit Dashboard
   |
   v
Cloudflare Worker API
   |
   +---- Workers AI
   |
   +---- D1 Database

## Important Technical Scope

The publicly deployed version currently uses:
- Keyword-based company-document retrieval from D1.
- Cloudflare Workers AI for answer generation.
- A native JavaScript function for order calculations.

The original Google Colab prototype separately explored LangGraph, Qwen, FAISS, customer memory, MCP and human-in-the-loop workflows. These are not all active components of the public deployment.

## Security

- API access protected using an application secret.
- Secrets are stored in hosting-platform configuration.
- Credentials and private customer information must never be committed to GitHub.

## Deployment

Frontend: Streamlit Community Cloud  
API: Cloudflare Workers  
Database: Cloudflare D1

## Project Status

Public portfolio demonstration successfully deployed and tested.

Further improvements include production-grade authentication, advanced semantic retrieval, remote MCP integration, persistent agent orchestration and expanded monitoring.

---

ABC Technologies Enterprise AI Capstone Project
