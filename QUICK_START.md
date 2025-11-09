# Tundra CLI - Quick Start

## Step 1: Install

```bash
cd backend
pip install -r requirements.txt
pip install -e .
playwright install
```

## Step 2: Start Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend starts at `http://localhost:8000`

## Step 3: Register & Login

Open a new terminal:

```bash
# Register (first time)
tundra register
# Enter username and password when prompted

# Login (returning users)
tundra login
# Enter username and password
```

## You're In! 🚀

```bash
# Check your account
tundra whoami

# View your jobs
tundra jobs

# Use the agents
tundra scrape https://finance.yahoo.com/quote/TSLA
tundra sentiment "This is amazing!"
```

---

## All Commands

### 🔐 Authentication
```bash
tundra register          # Create account with username/password
tundra login             # Login with credentials
tundra logout            # Logout
tundra whoami            # Show your account & stats
```

### 📊 View Your Activity
```bash
tundra jobs              # List your recent jobs
tundra jobs --limit 20   # Show more jobs
tundra status <job_id>   # View specific job details
```

### 🤖 Agent Commands
```bash
tundra scrape <url> [--goal "description"]
tundra sentiment "your text"
tundra execute <task> --url <url>
tundra orchestrate "complex query"
tundra job <task> [--url <url>]  # Submit to queue
```

### ⚙️ Utilities
```bash
tundra health           # Check backend status
tundra config-show      # Show configuration
tundra --help           # See all commands
```

---

## Examples

### Register & First Task
```bash
$ tundra register
Username: alice
Password: ********
Repeat for confirmation: ********

✅ Registration successful!
👤 Username: alice

✨ You are now logged in and ready to use Tundra!

$ tundra scrape https://finance.yahoo.com/quote/AAPL
🌐 Scraping URL: https://finance.yahoo.com/quote/AAPL
✅ Scraping completed!
...
```

### Check Your Account
```bash
$ tundra whoami

👤 User: alice
📅 Joined: 2025-01-15T10:30:00
🕐 Last Active: 2025-01-15T11:45:00

📊 Your Stats:
   Total Jobs: 15
   Pending: 2
   Completed: 13
```

### View Your Jobs
```bash
$ tundra jobs

📋 Your Recent Jobs (5 shown):

1. ✅ Scrape Tesla stock data
   Job ID: abc123
   Status: completed
   Created: 2025-01-15T11:30:00
   Agent: WebScraperAgent

2. ⏳ Analyze sentiment
   Job ID: def456
   Status: pending
   Created: 2025-01-15T11:45:00

💡 View job details: tundra status <job_id>
```

---

That's it! Login with username & password, see all your active jobs. 🎉
