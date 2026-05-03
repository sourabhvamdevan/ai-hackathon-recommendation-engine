## Project Overview: BIS Standard Discovery Engine

The BIS Standard Discovery Engine is an AI-powered Recommendation Engine designed to assist Indian Micro and Small Enterprises (MSEs) in identifying applicable Bureau of Indian Standards (BIS) regulations. By utilizing a Retrieval-Augmented Generation (RAG) pipeline, the system converts complex product descriptions into accurate standard recommendations within seconds, focusing specifically on the Building Materials category (Cement, Steel, Concrete, and Aggregates).

---

## System Architecture

The solution implements a decoupled architecture consisting of a React frontend and a Python-based FastAPI backend. 

*   **Frontend:** Built with React, providing a glassmorphic dashboard for user input and clear display of regulatory rationales.
*   **Backend:** Powered by FastAPI, managing the orchestration between the user interface and the RAG engine.
*   **RAG Engine:** Utilizes LangChain for document processing and FAISS (Facebook AI Similarity Search) for high-performance vector retrieval.
*   **LLM:** Integrated with OpenAI GPT-4o-mini to generate context-aware rationales while maintaining low latency.

---

## Technical Features

*   **Hybrid Retrieval Strategy:** Combines semantic vector search with regex-based standard ID extraction to ensure high Hit Rate @3 and MRR @5.
*   **Optimized Chunking:** Implements RecursiveCharacterTextSplitter with domain-specific separators to maintain the integrity of regulatory clauses.
*   **Inference CLI:** Includes a mandatory entry-point script (inference.py) for automated evaluation against private datasets.
*   **Containerization:** Fully Dockerized environment to ensure reproducibility and ease of deployment.

---

## Repository Structure

```text
/ai-hackathon-submission-bis
│
├── backend/
│   ├── src/
│   │   └── rag_engine.py      # Core RAG logic and vector store management
│   ├── data/                  # BIS SP 21 Building Material PDF documents
│   ├── main.py                # FastAPI server and API endpoints
│   ├── inference.py           # Mandatory evaluation entry point
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container definition
│   └── .env                   # Environment variables (OpenAI API Key)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main dashboard interface
│   │   └── App.css            # Styles and glassmorphic UI definitions
│   └── package.json           # Node.js dependencies
│
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # Project documentation
```

---

## Installation and Setup

### Prerequisites
*   Docker and Docker Compose
*   OpenAI API Key

### Configuration
1.  Navigate to the backend directory.
2.  Create a .env file.
3.  Add your API key: `OPENAI_API_KEY=your_api_key_here`

### Running the Project with Docker
From the root directory, execute:
```bash
docker-compose up --build
```
The backend will be accessible at http://localhost:8000 and the frontend at http://localhost:5173.

---

## Evaluation Procedure

The project includes a standardized inference script for performance benchmarking. To run the automated evaluation:

```bash
python backend/inference.py --input <path_to_input_json> --output <path_to_output_json>
```

The script processes query-result pairs and generates a JSON file containing retrieved standard IDs and latency metrics, which is compatible with the mandatory eval_script.py.

---

## Performance Metrics

*   **Hit Rate @3:** Target > 80%
*   **MRR @5:** Target > 0.7
*   **Average Latency:** < 5 seconds per query

---

## Team Acknowledgements

*   Team Name: Sigma Squad
*   Track: AI / Retrieval Augmented Generation (RAG)
*   Event: BIS x Sigma Squad AI Hackathon 2026
