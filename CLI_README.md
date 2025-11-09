# Tundra CLI - Complete Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Playwright Browsers (Required for Web Scraping)

```bash
playwright install
```

### 3. Install the CLI

```bash
pip install -e .
```

This will install the `tundra` command globally on your system.

### 4. Start the Backend Server

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

---

## 📖 Usage Guide

### Authentication Commands

#### Register a New User
```bash
tundra register <username>
```

Example:
```bash
tundra register john_doe
```

Output:
```
✅ Registration successful!
📋 User ID: john_doe
🔑 API Key: tundra_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
⚠️  API key generated successfully. Save this key securely - you won't be able to see it again!
✨ You are now logged in and ready to use Tundra!
```

**Important:** Save your API key! It's stored in `~/.tundra/config.json` for CLI use.

#### Login (Generate New API Key)
```bash
tundra login <username>
```

This will:
- Deactivate your old API keys
- Generate a new API key
- Save it to your config

#### Logout
```bash
tundra logout
```

Revokes your current API key and clears local configuration.

#### Check Current User
```bash
tundra whoami
```

Shows your current user ID and API key (masked).

---

### Agent Commands

#### 1. Execute Task Immediately
```bash
tundra execute <task_type> [OPTIONS]
```

**Options:**
- `--url <url>`: URL to scrape or analyze
- `--text <text>`: Text to analyze
- `--goal <goal>`: Goal or objective for the task

**Examples:**

```bash
# Web scraping
tundra execute web_scrape --url https://finance.yahoo.com/quote/TSLA --goal "Get Tesla stock price and news"

# Sentiment analysis
tundra execute sentiment_analysis --text "This product is amazing! I love it."

# Custom task with goal
tundra execute summarize --url https://example.com/article --goal "Summarize the main points"
```

#### 2. Scrape a Website
```bash
tundra scrape <url> [--goal <description>]
```

**Examples:**

```bash
# Scrape Tesla stock information
tundra scrape https://finance.yahoo.com/quote/TSLA

# Scrape with specific goal
tundra scrape https://finance.yahoo.com/quote/AAPL --goal "Get current stock price and latest news"

# Scrape product information
tundra scrape https://www.anthropic.com/claude --goal "Get pricing information"
```

#### 3. Analyze Sentiment
```bash
tundra sentiment <text>
```

**Examples:**

```bash
tundra sentiment "The stock market crashed today, investors are worried."

tundra sentiment "Amazing product! Best purchase I've made this year!"
```

#### 4. Submit Job (Async Queue)
```bash
tundra job <task_description> [OPTIONS]
```

**Options:**
- `--url <url>`: URL to include
- `--wait`: Wait for completion (polls for results)

**Examples:**

```bash
# Submit a job to the queue
tundra job "Analyze Tesla stock sentiment" --url https://finance.yahoo.com/quote/TSLA

# Submit and wait for results
tundra job "Get Apple stock data" --url https://finance.yahoo.com/quote/AAPL --wait
```

#### 5. Multi-Agent Orchestration
```bash
tundra orchestrate <complex_query>
```

This command uses multiple agents in sequence based on the query.

**Examples:**

```bash
tundra orchestrate "Get Tesla stock news and analyze the sentiment"

tundra orchestrate "Scrape Apple stock data and summarize the key information"
```

---

### Configuration Commands

#### Set API URL
```bash
tundra config-set-url <url>
```

Example:
```bash
tundra config-set-url http://localhost:8000
tundra config-set-url https://api.tundra.com
```

#### Show Configuration
```bash
tundra config-show
```

Output:
```
⚙️  Tundra Configuration:

🌐 API URL: http://localhost:8000
📋 User ID: john_doe
🔑 API Key: tundra_xxxxxxxx...xxxxxxxxxx

📁 Config file: /home/user/.tundra/config.json
```

#### Check API Health
```bash
tundra health
```

Checks if the Tundra backend is running and healthy.

---

## 🎯 Complete Examples

### Example 1: Stock Analysis Workflow

```bash
# 1. Register
tundra register alice

# 2. Scrape Tesla stock data
tundra scrape https://finance.yahoo.com/quote/TSLA --goal "Get current price and news"

# 3. Analyze sentiment of news
tundra sentiment "Tesla stock surges on strong earnings report"

# 4. Full orchestration
tundra orchestrate "Analyze Tesla stock news sentiment"
```

### Example 2: Web Research

```bash
# Login
tundra login bob

# Scrape multiple sources
tundra scrape https://www.anthropic.com/claude --goal "Get Claude API pricing"

# Execute custom task
tundra execute web_scrape --url https://openai.com/pricing --goal "Get GPT-4 pricing"
```

### Example 3: Async Job Processing

```bash
# Submit multiple jobs
tundra job "Analyze AAPL stock" --url https://finance.yahoo.com/quote/AAPL
tundra job "Analyze GOOGL stock" --url https://finance.yahoo.com/quote/GOOGL
tundra job "Analyze MSFT stock" --url https://finance.yahoo.com/quote/MSFT

# Jobs process in background queue
```

---

## 🔧 Available Task Types

- `web_scrape`: Scrape data from websites using browser automation
- `sentiment_analysis`: Analyze sentiment of text
- `summarize`: Summarize content or data
- Custom tasks: The TundraAgent will route to appropriate agents

---

## 🗂️ Configuration Storage

CLI configuration is stored in:
- **Linux/Mac**: `~/.tundra/config.json`
- **Windows**: `C:\Users\<username>\.tundra\config.json`

Configuration includes:
```json
{
  "api_url": "http://localhost:8000",
  "api_key": "tundra_xxxxxxxxxxxxxxxxxx",
  "user_id": "your_username"
}
```

---

## 🔐 API Key Security

- API keys are hashed (SHA-256) before storage in the database
- Never commit your API key to version control
- API keys are stored locally in `~/.tundra/config.json`
- Use `tundra logout` to revoke keys when done
- Generate new keys with `tundra login` if compromised

---

## 🛠️ Troubleshooting

### Cannot Connect to API

```bash
❌ Cannot connect to Tundra API at http://localhost:8000
💡 Make sure the backend is running with: uvicorn main:app --reload
```

**Solution:** Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

### Authentication Required

```bash
❌ Not authenticated. Please run 'tundra login' or 'tundra register' first.
```

**Solution:** Register or login:
```bash
tundra register your_username
```

### Playwright Issues

If web scraping fails:
```bash
playwright install
```

---

## 📋 Command Reference

| Command | Description |
|---------|-------------|
| `tundra register <user_id>` | Register new user and get API key |
| `tundra login <user_id>` | Login and generate new API key |
| `tundra logout` | Logout and revoke API key |
| `tundra whoami` | Show current user info |
| `tundra execute <task>` | Execute task immediately |
| `tundra scrape <url>` | Scrape website data |
| `tundra sentiment <text>` | Analyze text sentiment |
| `tundra job <task>` | Submit async job to queue |
| `tundra orchestrate <query>` | Multi-agent orchestration |
| `tundra config-set-url <url>` | Set API URL |
| `tundra config-show` | Show configuration |
| `tundra health` | Check API health |
| `tundra --help` | Show help message |

---

## 🎉 You're All Set!

Your Tundra CLI is ready to use. Start by registering:

```bash
tundra register your_username
```

Then try your first command:

```bash
tundra scrape https://finance.yahoo.com/quote/TSLA --goal "Get Tesla stock price"
```

Happy coding! 🚀
