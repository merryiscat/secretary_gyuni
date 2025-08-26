# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Secretary Gyuni (식사비서 재규니) is a Korean food recommendation assistant built with LangGraph and LangChain. The application classifies user intents and provides restaurant recommendations or casual conversation responses.

## Architecture

### Core Components

- **Graph.py**: Main LangGraph workflow definition using StateGraph with conditional routing
- **State.py**: TypedDict state definitions for the graph workflow (`InputState`, `OverallState`, `EndState`)
- **Node.py**: Individual graph nodes implementing business logic with structured logging decorators
- **Mcp_Tool.py**: MCP (Model Context Protocol) integration for external API calls

### Workflow Flow

1. **user_input_node**: Processes initial user input
2. **intent_classify**: Classifies intent into 4 categories (음식추천요청, 식당검색요청, 일상대화, 정체성문의)
3. **Conditional routing** based on intent:
   - **Food recommendation**: `food_recommand_node` → end
   - **Restaurant search**: `intent_extract` → `keywords_rank` → `query_make` → `run_mcp` → `result_make`
   - **Casual chat**: `talk_node` → end
   - **Identity query**: `identity_node` → end

### Chain Architecture

Located in `app/chain/`, each chain follows the pattern:
- Prompt template loaded from text files in `app/chain/prompt/`
- LangChain pipeline: `ChatPromptTemplate | ChatOpenAI | JsonOutputParser`
- Structured output using TypedDict schemas

### External Dependencies

- **MCP Server**: Restaurant search via n8n webhook (localhost:5678)
- **Kakao Map API**: Place recommendations through Smithery.ai MCP server
- **OpenAI GPT-4o-mini**: Primary LLM for all chains

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -e .

# Set required environment variables
OPENAI_API_KEY=your_key
KAKAO_MAP_API_KEY=your_key  
SMITHERY_API_KEY=your_key
```

### Running the Application
```bash
# Start Streamlit UI
streamlit run UI/main.py

# Ensure MCP dependencies are running:
# - n8n webhook server on localhost:5678
# - Smithery.ai MCP server accessible
```

### Logging and Debugging

The application uses structured JSON logging via `app/logger/`:
- Logs stored in `logs/app.jsonl`
- Node execution logging with `@log_node_outputs` decorators
- Configurable output limits for large data structures

### Key Configuration Files

- **pyproject.toml**: Project dependencies and metadata
- **mcp.config**: MCP server configuration for naver_web_search
- **app/chain/prompt/*.txt**: Prompt templates for each chain

### State Management

The application maintains state through the LangGraph workflow:
- User input and intent classification
- Location and food preferences extraction
- Search results and final recommendations
- Conversation history and exit messages

## External Service Dependencies

1. **n8n Workflow**: Restaurant search webhook at `http://localhost:5678/webhook/76b4d5d4-57a9-46af-ae0c-66fa0fcc3e46`
2. **Smithery.ai MCP**: Kakao Map integration via `https://server.smithery.ai/@cgoinglove/mcp-server-kakao-map/mcp`
3. **OpenAI API**: All LLM operations use GPT-4o-mini model