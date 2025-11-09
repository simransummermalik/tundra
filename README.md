# Tundra CLI

**Transactional Unified Network for Distributed Recursive Agents**
**A2A Marketplace Command-Line Interface**

Version 1.0.0

---

## Quick Installation

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt
pip install -e .
playwright install

# 2. Start backend
uvicorn main:app --reload

# 3. Welcome! (in new terminal)
tundra welcome
```

---

## First Steps

```bash
# Register
tundra register
Username: yourname
Password: ********

# Check account
tundra whoami

# Try first command
tundra scrape https://finance.yahoo.com/quote/TSLA
```

---

## Features

- **Username/Password Authentication** - Secure login with bcrypt
- **API Key Management** - Automatic generation and rotation
- **Web Scraping** - Intelligent data extraction with AI
- **Sentiment Analysis** - Analyze text sentiment
- **Multi-Agent Orchestration** - Complex workflows
- **Job Queue** - Async task processing
- **User Dashboard** - View stats and job history

---

## All Commands

### Authentication
- `tundra register` - Create account
- `tundra login` - Login
- `tundra logout` - Logout
- `tundra whoami` - Account info

### Agents
- `tundra scrape <url>` - Web scraping
- `tundra sentiment <text>` - Sentiment analysis
- `tundra execute <task>` - Custom tasks
- `tundra orchestrate <query>` - Multi-agent

### Jobs
- `tundra jobs` - List jobs
- `tundra job <task>` - Submit job
- `tundra status <id>` - Check status

### Utilities
- `tundra welcome` - Getting started guide
- `tundra health` - Check API
- `tundra --help` - Full help
- `tundra --version` - Version

---

## Documentation

- **[FINAL_DOCUMENTATION.md](FINAL_DOCUMENTATION.md)** - Complete documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[CLI_README.md](CLI_README.md)** - Detailed CLI reference

---

## Example Usage

```bash
# Register and login
$ tundra register
Username: alice
Password: ********
[OK] Registration successful!

# View your account
$ tundra whoami
User: alice
Stats:
   Total Jobs: 0
   Pending: 0
   Completed: 0

# Scrape a website
$ tundra scrape https://finance.yahoo.com/quote/AAPL
[OK] Scraping completed!
...

# Analyze sentiment
$ tundra sentiment "This is amazing!"
[OK] Sentiment: positive
[OK] Score: 0.95

# View your jobs
$ tundra jobs
Jobs: Your Recent Jobs (2 shown):
1. [OK] Scrape Apple stock
2. [PENDING] Analyze sentiment
```

---

## Architecture

**Backend:** FastAPI + MongoDB + Azure OpenAI
**CLI:** Click + Requests + bcrypt
**Agents:** Playwright + AI-powered extraction

---

## Support

Run `tundra welcome` for getting started guide
Run `tundra --help` for command reference

---

**Built for the Tundra A2A Marketplace**
