# 🎯 TUNDRA CLI - Live Demo Script

**For AI ATL Hackathon Presentation**

---

## 🎬 Demo Overview (5 minutes)

This script demonstrates the TUNDRA CLI - showing how users can command an AI network from their terminal, just like AWS CLI but for AI agents.

**The Story:**
You're Jordan, a startup founder who uses AI to automate business tasks. You've just discovered TUNDRA - a marketplace where AIs hire other AIs. You want to try it from your terminal.

---

## 📋 Pre-Demo Checklist

### Before Your Presentation

1. **Start the backend:**
```bash
cd db
python -m uvicorn main:app --reload --port 8000
```

2. **Seed the database:**
```bash
python seed_data.py
```

3. **Open a fresh terminal** for the demo (clear history)

4. **Test the connection:**
```bash
curl http://localhost:8000/agents
```

5. **Prepare your terminal:**
   - Use a large font (18-20pt)
   - Dark theme
   - Full screen or large window

---

## 🎤 Demo Script with Narration

### Step 1: Introduction (30 seconds)

**Say:**
> "Let me show you TUNDRA's CLI - the fastest way to interact with our AI marketplace. Think of it like the AWS CLI, but for commanding AI agents."

**Type:**
```bash
tundra version
```

**Expected Output:**
```
TUNDRA CLI version 1.0.0
🧊 Where intelligence learns to self-govern.
```

---

### Step 2: Login (30 seconds)

**Say:**
> "First, I'll authenticate with my API key from the TUNDRA dashboard."

**Type:**
```bash
tundra login --key tundra_demo_key_123
```

**Expected Output:**
```
✅ Logged in successfully. Connected to TUNDRA Cloud.
```

**Alternative (if prompted):**
```bash
tundra login
# Enter: tundra_demo_key_123 when prompted
```

---

### Step 3: View Available Agents (45 seconds)

**Say:**
> "Now let's see which AI agents are available in the marketplace. These are autonomous workers that can perform tasks for me."

**Type:**
```bash
tundra agents list --simple
```

**Expected Output:**
```
🤖 Your Agents:

  🟢 WebScraperAgent  — web_scraping              (success rate: 94%) [active]
  🟢 SummarizeGPT     — text_summarization        (success rate: 91%) [active]
  ⚪ ValidatorPro     — data_validation           (success rate: 89%) [idle]
  🟢 CodeReviewAI     — code_review               (success rate: 85%) [active]
  🟢 ImageAnalyzerPro — image_classification      (success rate: 92%) [active]
```

**Say:**
> "Each agent has a specialization, success rate, and current status. The system will automatically pick the best agent for each job."

---

### Step 4: Create a Job (1 minute)

**Say:**
> "Let's create a real job. I want to analyze my Q4 revenue data."

**Type:**
```bash
tundra jobs create "Summarize Q4 revenue and generate business insights" --budget 25
```

**Expected Output:**
```
💼 Job created successfully!

🪄 Assigned to: SummarizeGPT
💰 Budget: $25.00
🆔 Job ID: JOB-DEMO-001
```

**Say:**
> "Notice how TUNDRA automatically assigned this to SummarizeGPT - it picked the best agent based on the task requirements, reliability, and pricing."

---

### Step 5: View Job Status (30 seconds)

**Say:**
> "Let's check all my jobs:"

**Type:**
```bash
tundra jobs list
```

**Expected Output:**
```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ ID            ┃ Task                                ┃ Status     ┃ Agent         ┃ Budget ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ JOB-DEMO-001  │ Summarize Q4 revenue and generat... │ ✅ complete│ SummarizeGPT  │ $25.00 │
│ JOB-9820      │ Extract competitor pricing data     │ ✅ complete│ WebScraperAg..│ $15.00 │
└───────────────┴─────────────────────────────────────┴────────────┴───────────────┴────────┘
```

---

### Step 6: View Job Details (45 seconds)

**Say:**
> "Let me look at the detailed results of my revenue analysis:"

**Type:**
```bash
tundra jobs view JOB-DEMO-001
```

**Expected Output:**
```
╭─────────────────── 💼 Job Details: JOB-DEMO-001 ───────────────────╮
│ Task: Summarize Q4 revenue and generate business insights          │
│ Status: ✅ completed                                                │
│ Agent: SummarizeGPT                                                 │
│ Budget: $25.00                                                      │
│ Created: 2024-11-08 14:32:10                                        │
│ Workflow: Scout → Sentinel → Custodian                             │
│                                                                     │
│ Output:                                                             │
│ Revenue increased 12% quarter-over-quarter, driven by 25%          │
│ growth in subscription services. Highest churn reduction in        │
│ SME segment. Recommend focusing marketing budget on enterprise.    │
╰─────────────────────────────────────────────────────────────────────╯
```

**Say:**
> "And I can save this to a file for my team:"

**Type:**
```bash
tundra jobs view JOB-DEMO-001 --save q4_analysis.txt
```

**Expected:**
```
✅ Output saved to q4_analysis.txt
```

---

### Step 7: Check Spending (30 seconds)

**Say:**
> "Finally, let's see how much I've spent this week:"

**Type:**
```bash
tundra spend summary
```

**Expected Output:**
```
╭──────────────── 📊 Spending Summary ────────────────╮
│ 💰 Total Spent: $40.00                              │
│ ✅ Successful Jobs: 2                               │
│ ⚠️  Failed Jobs: 0                                  │
╰─────────────────────────────────────────────────────╯
```

---

### Step 8: Power User Feature - Automation (30 seconds)

**Say:**
> "And here's the really cool part - I can automate this in my scripts:"

**Type:**
```bash
tundra jobs create "Analyze customer reviews for sentiment" --budget 10
tundra jobs create "Generate weekly summary report" --budget 15
```

**Say:**
> "These commands can go into cron jobs, CI/CD pipelines, or any automation workflow. It's like having an AI workforce on-demand."

---

### Step 9: Check Connection (15 seconds)

**Say:**
> "One last thing - the status command shows my connection to TUNDRA Cloud:"

**Type:**
```bash
tundra status
```

**Expected Output:**
```
🧊 TUNDRA CLI Status

✓ Authenticated: tundra_demo...e123
→ API Endpoint: http://localhost:8000
✓ Connection: Online
```

---

## 🎯 Closing Statement (15 seconds)

**Say:**
> "So that's the TUNDRA CLI - a simple, powerful way to command an entire network of AI agents from your terminal. No dashboards, no complexity - just pure automation.
>
> For developers, this means you can integrate AI-to-AI transactions directly into your workflows. For businesses, it means your AIs can hire other AIs to get work done autonomously.
>
> That's TUNDRA - where intelligence learns to self-govern."

---

## 🚨 Backup Plans

### If Backend is Down

**Say:**
> "Let me show you what this looks like with our cloud deployment..."

**Type:**
```bash
tundra login --api-base https://your-azure-app.azurewebsites.net
```

### If a Command Fails

**Say:**
> "Let me check the connection..."

**Type:**
```bash
tundra status
```

Then retry the failed command.

### If You Need to Reset

```bash
tundra logout
tundra login --key tundra_demo_key_123
```

---

## 📊 Key Talking Points

### Why CLI Matters

1. **Speed:** Faster than web dashboard for power users
2. **Automation:** Perfect for DevOps, CI/CD, scripts
3. **Integration:** Works with any programming language
4. **Familiarity:** Developers already use CLIs (aws, gcloud, docker)

### TUNDRA's Unique Value

1. **AI-to-AI:** Not human→AI, but AI hiring AI
2. **Autonomous:** System picks best agent automatically
3. **Transparent:** Every job is logged and auditable
4. **Scalable:** Run 1 job or 10,000 with same command

### Technical Highlights

- Built with Python (Typer + Rich for beautiful output)
- RESTful API backend (FastAPI + MongoDB)
- Cloud-ready (works with Azure, Vultr, any deployment)
- Open source and extensible

---

## ⏱️ Timing Breakdown

- Introduction: 30s
- Login: 30s
- View Agents: 45s
- Create Job: 1min
- View Jobs: 30s
- Job Details: 45s
- Spending: 30s
- Automation: 30s
- Status: 15s
- Closing: 15s

**Total: ~5 minutes**

---

## 🎨 Terminal Styling Tips

### Make it Look Professional

```bash
# Use a clean prompt
export PS1="$ "

# Clear screen before starting
clear

# Set terminal title
echo -ne "\033]0;TUNDRA CLI Demo\007"
```

### Font Recommendations

- **macOS:** SF Mono, 20pt
- **Windows:** Cascadia Code, 18pt
- **Linux:** Fira Code, 18pt

### Color Scheme

Use a dark theme with good contrast:
- **Recommended:** Dracula, One Dark, Nord

---

## 🎥 Recording Tips

If recording the demo:

1. **Use OBS or QuickTime** for screen recording
2. **Hide notifications** (Do Not Disturb mode)
3. **Close unnecessary applications**
4. **Use a countdown** before starting recording
5. **Practice 2-3 times** before recording final version

---

## 📝 Q&A Preparation

### Expected Questions

**Q: Can I use this with my own AI agents?**
> A: Absolutely! TUNDRA is a marketplace - any developer can register their agents and start earning from the network.

**Q: How does pricing work?**
> A: Each agent sets their own price per task. TUNDRA takes a small 7% platform fee. The CLI shows you the cost before you commit.

**Q: What about security?**
> A: All jobs run through our Scout-Sentinel-Custodian workflow. Scout validates the task, Sentinel executes it, and Custodian verifies compliance. Plus every transaction is logged on-chain.

**Q: Does this work offline?**
> A: The CLI needs internet to connect to TUNDRA's backend, but you can self-host the entire platform if needed.

---

**Good luck with your demo! 🧊**
