# 📈 FastB3 API

A modern, high-performance **RESTful API** for retrieving **stock and ETF data** from **B3 (Brazilian Stock Exchange)**.

Built with **Python and FastAPI**, FastB3 works as a **financial microservice** that consumes market data, processes relevant information, and returns a standardized, typed, and validated JSON payload.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688?style=flat-square\&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square\&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square\&logo=docker)](https://docker.com)

---

## 📚 Table of Contents

- [📌 Description](#description)
- [✨ Features](#features)
- [🛠 Technologies](#technologies)
- [🏗 Architecture](#architecture)
- [⚙️ Installation](#installation)
- [📖 API Usage](#api-usage)
- [📊 Data Model](#data-model)
- [🧪 Tests](#tests)
- [📁 Project Structure](#project-structure)
- [⚙️ Technical Details](#technical-details)
- [🤝 Contributing](#contributing)
- [⚠️ Disclaimer](#disclaimer)

# 📌 Description <a id="description"></a>

The **FastB3 API** simplifies access to market data for:

* stocks (ações)
* ETFs (Exchange Traded Funds)

traded on the Brazilian stock exchange (B3).

It acts as an intermediary layer that:

* fetches market data via **Yahoo Finance**
* standardizes the information
* calculates relevant metrics
* returns structured JSON responses

The API is designed to be used in:

* financial applications
* market dashboards
* investment analysis systems
* financial data microservices

---

# ✨ Features <a id="features"></a>

* 📊 **Real-time stock and ETF quotes**
* 🔎 **Support for any B3 ticker (stocks & ETFs)**
* ➕ **Automatic `.SA` suffix handling**
* 📉 **Absolute and percentage change calculations**
* 🔢 **Financial precision using `Decimal`**
* 🧾 **Typed responses with Pydantic**
* ⚠️ **Robust error handling**
* 🐳 **Docker-ready deployment**

---

# 🛠 Technologies <a id="technologies"></a>

| Technology       | Description                           |
| ---------------- | ------------------------------------- |
| **Python 3.10+** | Main programming language             |
| **FastAPI**      | Modern high-performance web framework |
| **Uvicorn**      | ASGI server                           |
| **Pydantic**     | Data validation and serialization     |
| **yfinance**     | Market data provider                  |
| **pytest**       | Testing framework                     |
| **Docker**       | Application containerization          |

---

# 🏗 Architecture <a id="architecture"></a>

The **FastB3 API** follows a **Layered Architecture** to ensure separation of concerns, testability, and maintainability.

Request flow:

1. The client sends an HTTP request
2. The **Router** receives the endpoint call
3. The **Service** executes the business logic
4. **yfinance** fetches data from Yahoo Finance
5. Data is normalized by **Schemas**
6. A JSON response is returned to the client

---

## Architecture Diagram

```mermaid
flowchart TD

Client["Client Application
(Web / Mobile / Script)"]

Router["FastAPI Router
(API Endpoints)"]

Service["Business Service
(Market Data Services)"]

External["Yahoo Finance API
(via yfinance)"]

Schema["Pydantic Schemas
Validation & Serialization"]

Response["JSON API Response"]

Client --> Router
Router --> Service
Service --> External
External --> Service
Service --> Schema
Schema --> Response
Response --> Client
```

---

# ⚙️ Installation <a id="installation"></a>

## Prerequisites

* Python **3.10+**
* pip
* Docker (optional)

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/herikerbeth/fastb3-api.git
cd fastb3
```

Create a virtual environment:

```bash
python -m venv venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

---

## Running with Docker

Build the image:

```bash
docker build -t fastb3-api .
```

Run the container:

```bash
docker run -p 8000:8000 fastb3-api
```

---

# 📖 API Usage <a id="api-usage"></a>

Once the application is running, access the interactive FastAPI documentation:

```
http://localhost:8000/docs
```

---

## Endpoints

### `GET /`

API health check.

**Response**

```json
{
  "message": "Welcome to FastB3 API"
}
```

---

### `GET /stock/{ticker}`

Retrieves the stock quote for a B3-listed company.

**Parameter**

| Name   | Type   | Description                      |
| ------ | ------ | -------------------------------- |
| ticker | string | Stock symbol (e.g. PETR4, VALE3) |

**Example**

```bash
curl http://localhost:8000/stock/PETR4
```

---

### Example Response

```json
{
  "data": {
    "symbol": "PETR4.SA",
    "open": "43.2500",
    "high": "44.2700",
    "low": "43.0100",
    "price": "43.9000",
    "volume": 47876000,
    "date": "2026-03-09",
    "previous_close": "42.1100",
    "change": "1.7900",
    "change_percent": "4.2508"
  }
}
```

---

### `GET /etf/{ticker}`

Retrieves detailed information for a B3-listed ETF.

**Parameter**

| Name   | Type   | Description                   |
| ------ | ------ | ----------------------------- |
| ticker | string | ETF symbol (e.g. GOLD11)      |

**Example**

```bash
curl http://localhost:8000/etf/GOLD11
```

---

### Example Response

```json
{
  "data": {
    "symbol": "GOLD11.SA",
    "name": "TREND OURO  CI",
    "price": "23.8400",
    "currency": "BRL",
    "market_cap": null,
    "sector": ""
  }
}
```

---

# 📊 Data Model <a id="data-model"></a>

| Field              | Type    | Description            |
| ------------------ | ------- | ---------------------- |
| symbol             | string  | Stock ticker           |
| open               | decimal | Opening price          |
| high               | decimal | Daily high             |
| low                | decimal | Daily low              |
| price              | decimal | Current price          |
| volume             | integer | Trading volume         |
| date               | date    | Last trading day       |
| previous_close     | decimal | Previous closing price |
| change             | decimal | Absolute change        |
| change_percent     | decimal | Percentage change      |

---

# 🧪 Tests <a id="tests"></a>

The project includes **unit and integration tests** using `pytest`.

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

---

# 📁 Project Structure <a id="project-structure"></a>

```
fastb3/
│
├── app/
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── quote_router.py
│   │   └── etf_router.py
│   │
│   ├── services/
│   │   ├── quote_service.py
│   │   └── etf_service.py
│   │
│   ├── schemas/
│   │   ├── quote_schema.py
│   │   └── etf_schema.py
│   └── utils/
│       └── finance.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── requirements.txt
├── Dockerfile
├── pytest.ini
└── README.md
```

---

# ⚙️ Technical Details <a id="technical-details"></a>

### Financial Precision

All monetary values use `Decimal` with **4 decimal places** to avoid common floating-point rounding errors.

### B3 Convention

Brazilian tickers automatically receive the suffix:

```
.SA
```

Example:

```
PETR4 → PETR4.SA
```

---

# 🤝 Contributing <a id="contributing"></a>

Contributions are welcome.

1. Fork the repository
2. Create a branch

```
git checkout -b feature/my-feature
```

3. Commit your changes

```
git commit -m "Add new feature"
```

4. Push to the branch

```
git push origin feature/my-feature
```

5. Open a Pull Request

---

# ⚠️ Disclaimer <a id="disclaimer"></a>

This project uses data from **Yahoo Finance** and **is not affiliated with B3 (Brasil Bolsa Balcão)**.