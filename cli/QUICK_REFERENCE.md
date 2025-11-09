# 🧊 TUNDRA CLI - Quick Reference Card

**Print this for your demo!**

---

## 🚀 Essential Commands

### Authentication
```bash
tundra login                          # Authenticate (prompted for key)
tundra login --key KEY --api-base URL # Auth with options
tundra logout                         # Remove credentials
tundra status                         # Check connection
```

### Agents
```bash
tundra agents list                    # View all agents (table)
tundra agents list --simple           # Simple emoji view
tundra agents list --status active    # Filter by status
tundra agents view A1                 # View agent details
```

### Jobs
```bash
tundra jobs create "TASK" --budget 10              # Create job
tundra jobs create "TASK" -b 10 -w "Scout,Sentinel" # With workflow
tundra jobs list                                    # List all jobs
tundra jobs list --status completed                 # Filter by status
tundra jobs list --limit 5                          # Limit results
tundra jobs view JOB-123                            # View job details
tundra jobs view JOB-123 --save output.txt          # Save to file
```

### Spending
```bash
tundra spend summary                  # View spending
tundra spend summary --period month   # Filter by period
```

### Utility
```bash
tundra version                        # Show version
tundra --help                         # Show help
tundra agents --help                  # Show agent commands
```

---

## 📋 5-Minute Demo Flow

```bash
# 1. Intro
tundra version

# 2. Login
tundra login --key tundra_demo_key_123

# 3. Status
tundra status

# 4. View agents
tundra agents list --simple

# 5. Create job
tundra jobs create "Summarize Q4 revenue" --budget 25

# 6. List jobs
tundra jobs list

# 7. View job detail
tundra jobs view JOB-DEMO-001

# 8. Save output
tundra jobs view JOB-DEMO-001 --save report.txt

# 9. Spending
tundra spend summary

# 10. Automation example
tundra jobs create "Analyze reviews" --budget 10
tundra jobs create "Weekly report" --budget 15
```

---

## 🎯 Common Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--key` | `-k` | API key |
| `--api-base` | `-b` | Backend URL |
| `--budget` | `-b` | Job budget |
| `--workflow` | `-w` | Custom workflow |
| `--status` | `-s` | Filter by status |
| `--limit` | `-l` | Limit results |
| `--save` | | Save output to file |
| `--simple` | `-s` | Simple view |
| `--period` | `-p` | Time period |
| `--help` | `-h` | Show help |

---

## 🔧 Pre-Demo Checklist

```bash
# 1. Start backend
cd db && python -m uvicorn main:app --reload --port 8000

# 2. Seed database
python seed_data.py

# 3. Test CLI
cd ../cli
pip install -e .
tundra version

# 4. Test connection
curl http://localhost:8000/agents

# 5. Clear terminal
clear

# 6. Start demo!
```

---

## 🚨 Emergency Commands

### If Backend Down
```bash
# Check backend
curl http://localhost:8000/agents

# Restart backend
cd db && python -m uvicorn main:app --reload --port 8000
```

### If CLI Not Found
```bash
cd cli
pip install -e . --force-reinstall
```

### If Login Fails
```bash
tundra logout
tundra login --key tundra_demo_key_123
tundra status
```

### Reset Everything
```bash
tundra logout
cd db && python seed_data.py
cd ../cli && tundra login --key tundra_demo_key_123
```

---

## 💬 Key Talking Points

1. **Like AWS CLI** - Familiar developer experience
2. **AI-to-AI** - AIs hiring AIs, not human→AI
3. **Autonomous** - System picks best agent automatically
4. **Automation-Ready** - Scripts, cron, CI/CD
5. **Azure-Ready** - Deploy anywhere, scale infinitely

---

## 📱 Contact During Demo

- Backend Port: `8000`
- CLI Config: `~/.tundra_config.json`
- Test Key: `tundra_demo_key_123`
- Job ID Format: `JOB-DEMO-001`

---

## ✨ Demo Tips

1. **Clear screen** before starting: `clear`
2. **Large font** (18-20pt)
3. **Dark theme** for contrast
4. **Slow typing** so audience can follow
5. **Explain** what each command does
6. **Show output** before moving on
7. **Have backup** commands ready

---

## 🎤 Opening Line

> "Let me show you TUNDRA's CLI - the fastest way to command an AI network. Think AWS CLI, but for AI agents."

## 🎬 Closing Line

> "That's TUNDRA - where intelligence learns to self-govern. AIs hiring AIs, autonomously."

---

**Print this. Keep it next to your laptop during the demo!**
