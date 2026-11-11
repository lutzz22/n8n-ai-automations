# n8n AI Automations

Three **n8n + OpenAI** automations based on real problems from the operations of electricity and gas utilities in Latin America, rebuilt from scratch with fictional data (the utility *VoltaSur Energía* and its regulator are invented).

| # | Workflow | Problem it solves | What it shows |
| --- | --- | --- | --- |
| 01 | [Jira (client) → Jira (internal) with AI](01-jira-to-jira-sync) | Incidents reported in the client's Jira were copied and rewritten by hand | Scheduled sync between two Jira sites, idempotent dedup, LLM analysis with a priority rubric, reply to the client, Slack alert |
| 02 | [Tariff table Excel → JSON](02-tariff-excel-to-json) | Each new regulator resolution meant copying dozens of values into the tariff JSON by hand | LLM used only for mapping labels, values copied by code, diff against production, anomaly detection before publishing |
| 03 | [AI Support Agent](03-ai-support-agent) | Repetitive customer questions about bills and outages | Tool-calling agent over Postgres, memory, human handoff, data access protected in SQL |

## Design principles

- **Structured output, never free text.** Every LLM step returns JSON validated against a schema, so the next node can trust the shape.
- **The LLM decides what language decides; code decides the rest.** Mapping labels, classifying and summarizing go to the model. Numbers, IDs, totals and routing rules go to code.
- **Nothing gets lost and nothing gets duplicated.** There are fallback paths when the model fails, idempotent syncs and review steps before anything risky is published.
- **Security lives outside the prompt.** The agent can only read an account if the SQL itself receives the account number *and* the holder's document digits.

## Run it locally

Requirements: Docker and an OpenAI API key.

```bash
git clone https://github.com/lutzz22/n8n-ai-automations.git
cd n8n-ai-automations
cp .env.example .env          # change the password
docker compose up -d          # n8n on http://localhost:5678 + Postgres with demo data
```

Then import each `workflow.json` (*Workflows → Import from file*), create the credentials each folder's README lists and publish.

| Workflow | Credentials |
| --- | --- |
| 01 | OpenAI, 2 × Jira Software Cloud (client + internal), Slack |
| 02 | OpenAI |
| 03 | OpenAI, Postgres (host `voltasur-db`, data from `.env`) |

## Tested

All three workflows were run end to end on n8n 2.x with the sample data in each folder:

- **01:** 3 client tickets. One was already synced and skipped; the other two were created with the right type, priority and labels, and the client was answered.
- **02:** the clean Excel produced the new JSON; the Excel with a typo was stopped with a review report.
- **03:** verification, invoices, outages and handoff were exercised through the chat.

## Stack

n8n · OpenAI · LangChain nodes (LLM Chain, Structured Output Parser, AI Agent) · Jira REST API · Slack · PostgreSQL · JavaScript · Docker

---

Built by **Lucía Arambarri** · [LinkedIn](https://www.linkedin.com/in/lucia-arambarri-791a37145/)
