# 🚀 TUNDRA CLI Installation Guide

## Quick Start (5 minutes)

### Step 1: Install the CLI

Navigate to the CLI directory and install in development mode:

```bash
cd cli
pip install -e .
```

This will:
- Install all dependencies (typer, requests, rich)
- Create the `tundra` command globally
- Allow you to edit the code and see changes immediately

### Step 2: Verify Installation

```bash
tundra version
```

You should see:
```
TUNDRA CLI version 1.0.0
🧊 Where intelligence learns to self-govern.
```

### Step 3: Start Your Backend

Make sure your FastAPI backend is running:

```bash
cd ../db
python -m uvicorn main:app --reload --port 8000
```

Or if deployed to Azure:
- Your backend will be at `https://your-app.azurewebsites.net`

### Step 4: Login

```bash
tundra login
```

When prompted, enter:
- **API Key:** Get from your TUNDRA dashboard Settings page (or use a test key like `tundra_sk_test123`)
- **API Base (optional):** Leave blank for localhost, or enter your Azure URL

For Azure deployment:
```bash
tundra login --key your_api_key --api-base https://tundra-api.azurewebsites.net
```

### Step 5: Test the CLI

```bash
# Check status
tundra status

# List agents
tundra agents list

# Create a test job
tundra jobs create "Test job from CLI" --budget 5

# View jobs
tundra jobs list
```

---

## For Demo/Presentation

### Pre-Demo Setup

1. **Seed the database** with sample agents:
```bash
cd ../db
python seed_data.py
```

2. **Start backend**:
```bash
python -m uvicorn main:app --reload --port 8000
```

3. **Open a new terminal** and test CLI commands

### Demo Script

```bash
# 1. Show authentication
tundra login --key demo_key_123

# 2. Check status
tundra status

# 3. List agents (simple view for quick demo)
tundra agents list --simple

# 4. Create a job
tundra jobs create "Summarize Q4 revenue and generate insights" --budget 25

# 5. List jobs
tundra jobs list

# 6. View spending
tundra spend summary
```

---

## Troubleshooting

### Command not found: tundra

The installation didn't complete. Try:
```bash
cd cli
pip install -e . --force-reinstall
```

### Import errors

Install dependencies manually:
```bash
pip install typer requests rich python-dotenv
```

### Backend connection fails

1. Check backend is running:
```bash
curl http://localhost:8000/agents
```

2. Update API base:
```bash
tundra login --api-base http://localhost:8000
```

---

## Deployment Checklist

### For Azure Cloud Deployment

- [ ] Deploy FastAPI backend to Azure App Service
- [ ] Get public URL (e.g., `https://tundra-api.azurewebsites.net`)
- [ ] Update CORS settings in `db/main.py` to allow CLI access
- [ ] Test connection: `curl https://your-app.azurewebsites.net/agents`
- [ ] Configure CLI: `tundra login --api-base https://your-app.azurewebsites.net`

### For Production PyPI Release

```bash
# Build the package
cd cli
python setup.py sdist bdist_wheel

# Upload to PyPI
pip install twine
twine upload dist/*
```

Then users can install with:
```bash
pip install tundra-cli
```

---

## Development Mode

If you're actively developing the CLI:

```bash
# Install in editable mode (already done with -e flag)
cd cli
pip install -e .

# Make changes to tundra_cli.py, utils.py, etc.
# Changes take effect immediately - no reinstall needed!

# Test your changes
tundra agents list
```

---

## Next Steps

1. **Customize branding:** Update colors/emojis in `utils.py`
2. **Add new commands:** Extend `tundra_cli.py` with new features
3. **Deploy to Azure:** Follow Azure deployment guide
4. **Share with team:** They just need to run `pip install -e .` from the cli folder

**Ready to command your AI network!** 🧊
