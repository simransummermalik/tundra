# Tundra CLI - Final Documentation

**Version:** 1.0.0
**A2A Marketplace Command-Line Interface**

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication)
4. [Commands Reference](#commands-reference)
5. [Usage Examples](#usage-examples)
6. [Configuration](#configuration)
7. [Architecture](#architecture)
8. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.8+
- MongoDB (cloud or local)
- Azure OpenAI API credentials

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Install Playwright (for web scraping)

```bash
playwright install
```

### Step 3: Install Tundra CLI

```bash
pip install -e .
```

This installs the `tundra` command globally on your system.

### Step 4: Configure Environment

Ensure `.env` file exists in the `backend` directory with:

```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
AZURE_DEPLOYMENT_NAME=your_deployment
MONGO_URI=your_mongodb_connection_string
```

### Step 5: Start Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000` by default.

---

## Quick Start

### First Time Setup

```bash
# Run welcome guide
tundra welcome

# Register new account
tundra register
Username: alice
Password: ********
Repeat for confirmation: ********

[OK] Registration successful!
User: Username: alice

You are now logged in and ready to use Tundra!
```

### First Command

```bash
# Check your account
tundra whoami

# Scrape a website
tundra scrape https://finance.yahoo.com/quote/TSLA

# View your jobs
tundra jobs
```

---

## Authentication

Tundra uses **username/password authentication** with secure API key generation.

### Register New Account

```bash
tundra register
```

- Prompts for username and password (with confirmation)
- Passwords are hashed with bcrypt before storage
- Generates and saves API key automatically
- You're logged in immediately after registration

### Login to Existing Account

```bash
tundra login
```

- Prompts for username and password
- Verifies credentials against database
- Generates new API key (old keys are revoked)
- Saves API key to `~/.tundra/config.json`

### Logout

```bash
tundra logout
```

- Revokes current API key
- Clears local configuration
- You'll need to login again to use the CLI

### Check Current User

```bash
tundra whoami
```

Shows:
- Username
- Join date
- Last activity
- Job statistics (total, pending, completed)

---

## Commands Reference

### Authentication Commands

| Command | Description |
|---------|-------------|
| `tundra register` | Create new account with username/password |
| `tundra login` | Login with existing credentials |
| `tundra logout` | Logout and revoke API key |
| `tundra whoami` | Show current user info and stats |

### Agent Commands

| Command | Description | Example |
|---------|-------------|---------|
| `tundra scrape <url>` | Scrape website data | `tundra scrape https://example.com` |
| `tundra scrape <url> --goal <desc>` | Scrape with specific goal | `tundra scrape https://news.com --goal "Get headlines"` |
| `tundra sentiment <text>` | Analyze sentiment | `tundra sentiment "Great product!"` |
| `tundra execute <task>` | Execute custom task | `tundra execute web_scrape --url https://example.com` |
| `tundra orchestrate <query>` | Multi-agent workflow | `tundra orchestrate "Get news and analyze sentiment"` |

### Job Management

| Command | Description | Example |
|---------|-------------|---------|
| `tundra jobs` | List recent jobs | `tundra jobs` |
| `tundra jobs --limit <n>` | Show more jobs | `tundra jobs --limit 20` |
| `tundra job <task>` | Submit async job | `tundra job "Scrape Tesla stock"` |
| `tundra status <job_id>` | Check job status | `tundra status abc123` |

### Utilities

| Command | Description |
|---------|-------------|
| `tundra welcome` | Show welcome guide |
| `tundra health` | Check backend API status |
| `tundra config-show` | Display configuration |
| `tundra config-set-url <url>` | Set API URL |
| `tundra --version` | Show CLI version |
| `tundra --help` | Show help message |

---

## Usage Examples

### Example 1: Basic Workflow

```bash
# 1. Register
$ tundra register
Username: bob
Password: ********
Repeat for confirmation: ********

[OK] Registration successful!
User: Username: bob

# 2. Check account
$ tundra whoami

User: bob
Joined: 2025-01-15T10:30:00

Stats:
   Total Jobs: 0
   Pending: 0
   Completed: 0

# 3. Scrape website
$ tundra scrape https://finance.yahoo.com/quote/AAPL --goal "Get stock price"

 Scraping URL: https://finance.yahoo.com/quote/AAPL
[OK] Scraping completed!
...
```

### Example 2: Job Queue

```bash
# Submit multiple jobs to queue
$ tundra job "Analyze Tesla stock" --url https://finance.yahoo.com/quote/TSLA

[OK] Job submitted successfully!
ID: Job ID: abc123
Status: queued

# Check all jobs
$ tundra jobs

Jobs: Your Recent Jobs (1 shown):

1. [PENDING] Analyze Tesla stock
   Job ID: abc123
   Status: pending
   Created: 2025-01-15T11:00:00

Tip: View job details: tundra status <job_id>

# Check specific job
$ tundra status abc123

[OK] Job Status: completed

Jobs: Job Details:
   ID: abc123
   Task: Analyze Tesla stock
   Created: 2025-01-15T11:00:00
   Agent: WebScraperAgent
   Finished: 2025-01-15T11:01:30

Tip: Reasoning: ...

Output: Output:
{
  "price": "$185.50",
  "change": "+2.3%",
  ...
}
```

### Example 3: Sentiment Analysis

```bash
$ tundra sentiment "The stock market crashed today. Investors are very worried."

[OK] Sentiment Analysis Complete!

Stats: Sentiment: negative
[OK] Score: -0.85

Output: Details:
{
  "keywords": ["crashed", "worried"],
  "confidence": 0.92
}
```

### Example 4: Multi-Agent Orchestration

```bash
$ tundra orchestrate "Get Apple stock news and analyze the sentiment"

[OK] Orchestration Complete!

Stats: Tundra Decision:
   Agent: WebScraperAgent
   Task Type: web_scrape
   Reasoning: First scrape news, then analyze sentiment

 Agents Used: 2

Jobs: Orchestration Log:

   Step 1: WebScraperAgent
   Action: Scraped web data

   Step 2: SentimentAgent
   Action: Analyzed sentiment of news

Output: Final Result:
{
  "scrape_data": {...},
  "sentiment_analysis": {...}
}
```

---

## Configuration

### Configuration File Location

- **Linux/Mac**: `~/.tundra/config.json`
- **Windows**: `C:\Users\<username>\.tundra\config.json`

### Configuration Format

```json
{
  "api_url": "http://localhost:8000",
  "api_key": "tundra_xxxxxxxxxxxxxxxxxx",
  "user_id": "your_username"
}
```

### Change API URL

```bash
# For local development
tundra config-set-url http://localhost:8000

# For production
tundra config-set-url https://api.tundra.com
```

### View Configuration

```bash
tundra config-show
```

Output:
```
 Tundra Configuration:

 API URL: http://localhost:8000
Jobs: User ID: alice
[OK] API Key: tundra_xxxxxxxx...xxxxxxxxxx

[OK] Config file: /home/user/.tundra/config.json
```

---

## Architecture

### Backend Components

1. **FastAPI Server** (`backend/main.py`)
   - REST API endpoints
   - Authentication system
   - Agent routing
   - Job queue management

2. **Database** (MongoDB)
   - Collections:
     - `users` - User accounts with hashed passwords
     - `api_keys` - API keys with hashed values
     - `jobs` - Job history and results

3. **Agent Executors** (`backend/agent_executor/`)
   - `WebScraperExecutor` - Web scraping with Playwright
   - `SentimentExecutor` - Sentiment analysis
   - `SummarizerExecutor` - Text summarization
   - `AgentExecutor` - Base class

4. **Event Queue** (`backend/agent_executor/event_queue.py`)
   - Tracks agent execution events
   - Provides execution history

### CLI Architecture

1. **Configuration Manager** (`TundraConfig` class)
   - Loads/saves config from `~/.tundra/config.json`
   - Manages API keys and URLs

2. **Command Groups**
   - Authentication commands
   - Agent operation commands
   - Job management commands
   - Utility commands

3. **API Client**
   - Makes HTTP requests to backend
   - Handles authentication headers
   - Error handling and user feedback

### Security Features

1. **Password Hashing**
   - Passwords hashed with bcrypt
   - Salt rounds: 12 (default)

2. **API Key Generation**
   - Format: `tundra_` + 32 URL-safe random characters
   - Hashed with SHA-256 before storage
   - Never displayed after initial generation

3. **API Key Authentication**
   - Passed in `X-API-Key` header
   - Verified on every protected endpoint
   - Last used timestamp updated

---

## Troubleshooting

### Cannot Connect to API

```
[ERROR] Cannot connect to Tundra API at http://localhost:8000
Tip: Make sure the backend is running with: uvicorn main:app --reload
```

**Solution:**
```bash
cd backend
uvicorn main:app --reload
```

### Authentication Required

```
[ERROR] Not authenticated. Please run 'tundra login' or 'tundra register' first.
```

**Solution:**
```bash
tundra login
# or
tundra register
```

### Invalid Username or Password

```
[ERROR] Invalid username or password
```

**Solution:**
- Check your username and password
- Register if you don't have an account: `tundra register`

### MongoDB Connection Error

If you see MongoDB connection errors in the backend logs:

1. Check your `MONGO_URI` in `.env` file
2. Ensure MongoDB is running (if using local MongoDB)
3. Verify network connectivity (if using MongoDB Atlas)

### Playwright Installation Issues

If web scraping fails:

```bash
playwright install
```

For specific browsers:
```bash
playwright install chromium
```

### Windows Encoding Issues

The CLI automatically handles Windows encoding. If you still see encoding errors:

1. Use Windows Terminal or PowerShell (not cmd.exe)
2. Set console to UTF-8: `chcp 65001`

---

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with credentials
- `DELETE /auth/revoke` - Revoke API key (requires auth)

### User Info

- `GET /me` - Get current user info and stats (requires auth)
- `GET /jobs` - List user's jobs (requires auth)
- `GET /jobs/{job_id}` - Get specific job (requires auth)

### Agent Operations

- `POST /submit_job` - Submit job to queue (requires auth)
- `POST /execute` - Execute task immediately (requires auth)
- `POST /orchestrate` - Multi-agent orchestration (requires auth)

### Utilities

- `GET /health` - Health check (public)
- `GET /` - Root endpoint (public)

---

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Starting Development Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Building Distribution

```bash
cd backend
python setup.py sdist bdist_wheel
```

### Installing Development Version

```bash
cd backend
pip install -e .
```

---

## Support

- **Documentation**: See `CLI_README.md` for detailed command reference
- **Quick Start**: See `QUICK_START.md` for getting started
- **Issues**: Report bugs or request features on GitHub

---

## Version History

### 1.0.0 (Current)
- Username/password authentication
- API key management
- Web scraping with Playwright
- Sentiment analysis
- Job queue system
- Multi-agent orchestration
- CLI with all core commands
- MongoDB integration
- Comprehensive documentation

---

## License

MIT License - See LICENSE file for details

---

**Tundra CLI - Built for the A2A Marketplace**
