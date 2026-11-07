# Project Case Study: ABC Technologies Enterprise AI Assistant

## Executive summary

ABC Technologies Enterprise AI is a portfolio demonstration of an enterprise-style assistant that answers questions about company policies and calculates customer orders. The project began as a hands-on Google Colab capstone combining language models, retrieval-augmented generation (RAG), customer memory, agent orchestration, tool calling, and Model Context Protocol (MCP) integration. A simplified version was then deployed publicly using Streamlit Community Cloud, Cloudflare Workers, Cloudflare Workers AI, and Cloudflare D1.

**Live demonstration:** https://abc-technologies-enterprise-ai-by-shahzad-panhwar.streamlit.app

**API health:** https://abc-technologies-enterprise-aii.panhwarshahzadali91.workers.dev/health

## Business problem

A small business support team may need to answer repetitive questions about refunds, order processing, and customer support while also performing straightforward order calculations. A useful assistant should retrieve information from company-approved documents, personalize the interaction with a customer profile, and produce consistent calculations.

This project demonstrates those workflows with synthetic company policies and sample customer profiles. It is an educational portfolio application, not a deployed system for a real company's live customer records.

## Users and demo scenarios

Two sample customers are stored in D1:

- Ahmed (`customer_001`): preferred currency PKR; preferred contact Email; sample unit price 350.
- Sara (`customer_002`): preferred currency USD; sample unit price 50; preferred contact Email.

The sample knowledge base contains:

1. Customer Refund Policy.
2. Order Processing Policy.
3. Customer Support Guidelines.

Representative user stories:

- As Ahmed, I can ask how long I have to request a refund and receive an answer grounded in the refund-policy record.
- As Sara, I can ask the same policy question while the system looks up her own profile.
- As a customer, I can request a calculation for a quantity and unit price and receive a total in my preferred currency.

## Solution overview

The deployed dashboard is built with Streamlit. It sends HTTPS requests to a Cloudflare Worker API protected by an application API key. The Worker retrieves customer profiles and company documents from D1. For policy questions, it ranks the small set of documents using keyword overlap and invokes Cloudflare Workers AI (`@cf/zai-org/glm-4.7-flash`) to generate a concise answer from the selected context. For order calculations, it validates the numeric inputs and performs the calculation in JavaScript.

## Architecture and technology choices

| Layer | Technology | Role in the deployed version |
|---|---|---|
| User interface | Streamlit Community Cloud | Dashboard, policy assistant, order calculator |
| API gateway and application logic | Cloudflare Workers | Authenticates and routes requests |
| AI inference | Cloudflare Workers AI, GLM-4.7-Flash | Generates policy answers |
| Structured storage | Cloudflare D1 | Customer profiles and policy documents |
| Source control | GitHub | Application code and deployment configuration |

The earlier Colab prototype additionally explored Qwen, FAISS, embeddings, reranking, LangGraph, customer memory isolation, MCP tools, and human-in-the-loop approval. Those features are not all part of the current public deployment.

## Selected workflow results

### Policy question

**Question:** How many days do I have to request a refund?

**Ground-truth policy:** Customers can request a refund within 7 calendar days after receiving their order.

**Reported deployed result:** The public API returned HTTP 200 and answered that the deadline is 7 calendar days from receipt of the order.

### Order calculation

**Input:** 8 items at PKR 350 each.

**Calculation:** 8 × 350 = 2,800.

**Reported deployed result:** The public API returned HTTP 200 with total `2800` and currency `PKR`.

### Security check

A request with an invalid API key returned HTTP 401, as expected.

The project owner also reported that the three dashboard scenarios (Overview/health, Policy Assistant, and Order Calculator) all produced the desired results.

## Validation summary

Manual functional checks reported on 7 November 2026:

| Check | Observed result |
|---|---|
| Public Worker health check | Healthy; D1 connected; two customer records; AI binding present |
| Policy API | HTTP 200; correct seven-calendar-day answer |
| Order API | HTTP 200; 2,800 PKR |
| Invalid API key | HTTP 401 |
| Unknown customer | HTTP 404 in earlier prototype security tests |
| Invalid quantity | HTTP 400 in earlier prototype security tests |
| Streamlit dashboard | Deployed and manually tested |

This is a manual functional test record, not a formal independent security, privacy, performance, or load evaluation.

## What worked well

- The system separates the dashboard from the server-side API and AI inference.
- Customer and policy records are stored in a database instead of being held only in notebook memory.
- The public Worker uses bindings for D1 and Workers AI.
- The API validates customer identifiers, request intent, question length, quantity, and unit-price ranges.
- The project includes a repeatable GitHub-based deployment workflow and publicly accessible demonstration URLs.

## Limitations and risks

- The deployed retriever uses simple keyword overlap over three D1 documents; it is not the original semantic FAISS retrieval system.
- The deployed order calculator is a native Worker function; it is not a remote MCP invocation.
- The public Worker routes requests directly; it does not currently execute the original LangGraph agent graph.
- The Qwen implementation remains in the Colab prototype; the public app uses Cloudflare Workers AI.
- Demo customer IDs are selected in the dashboard. There is no robust individual login, identity verification, or tenant-level authorization yet.
- The application should not process real refunds, financial transactions, or sensitive customer data in its current state.
- Free-tier quotas, model availability, and service limits can change and should be monitored.

## Next improvements

1. Add customer authentication and authorization with per-customer data isolation.
2. Add rate limiting, stricter CORS, structured audit logs, and request monitoring.
3. Improve retrieval with embeddings, vector search, or Cloudflare AI Search if appropriate for the hosting limits.
4. Deploy a genuine remote MCP server and call it through the MCP protocol rather than using a local Worker function for all actions.
5. Reintroduce LangGraph orchestration in the deployed architecture where its stateful routing and checkpointing add measurable value.
6. Add approval gates for consequential actions such as refunds and order changes.
7. Add scheduled database backups, operational alerts, and more comprehensive automated tests.

## Portfolio description

**ABC Technologies Enterprise AI Assistant** — Built and deployed a serverless enterprise AI demonstration using Streamlit, Cloudflare Workers, Workers AI, and D1. The application supports grounded company-policy Q&A, customer-profile lookup, authenticated API requests, and validated order calculations. The broader Colab capstone explored Qwen, RAG, FAISS, LangGraph, MCP, memory isolation, and human-in-the-loop workflows.

## Suggested resume bullet

Built and deployed a public enterprise AI demo using Streamlit, Cloudflare Workers AI, and D1, implementing document-grounded policy Q&A, customer-profile retrieval, API-key authentication, and validated business calculations; separately prototyped RAG, LangGraph, MCP tool calling, and human-in-the-loop workflows in Google Colab.
