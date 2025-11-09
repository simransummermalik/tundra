# TUNDRA Integration Guide

This guide explains how to start and test the fully integrated TUNDRA application.

## Architecture Overview

- **Frontend**: React application with Supabase authentication
- **Backend**: FastAPI server with MongoDB and Azure OpenAI
- **Database**: MongoDB Atlas for job queue and agent management
- **Authentication**: Supabase for user authentication

## Prerequisites

1. Node.js and npm installed
2. Python 3.8+ installed
3. MongoDB Atlas connection configured
4. Azure OpenAI API access configured
5. Supabase project set up

## Environment Configuration

### Frontend Configuration

Location: `frontend/.env`

```env
REACT_APP_SUPABASE_URL=https://aojryactwieksvynfzil.supabase.co/
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key_here
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Backend Configuration

Location: `backend/.env`

```env
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_DEPLOYMENT_NAME=your_deployment_name
MONGO_URI=your_mongodb_connection_string
MARKETPLACE_ENABLED=1
```

## Starting the Application

### 1. Start the Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend will start on http://localhost:8000

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm start
```

The frontend will start on http://localhost:3000

## Testing the Integration

### Test 1: Backend Health Check

Open http://localhost:8000 in your browser. You should see:
```json
{"message": "TUNDRA Requester Agent running"}
```

Check the marketplace status:
http://localhost:8000/marketplace/status

### Test 2: Agents Endpoint

http://localhost:8000/agents

Should return a list of agents including:
- WebScraperAgent
- SummarizerAgent
- SentimentAgent
- OrchestratorAgent

### Test 3: Frontend Login

1. Open http://localhost:3000
2. You should see the TUNDRA login page
3. Log in using your Supabase credentials

### Test 4: Submit a Job

1. Navigate to the "Jobs" page
2. Click on "New" tab
3. Enter a task description, for example:
   - "Get the current stock price for Tesla"
   - "Analyze the sentiment of recent Tesla news"
   - "Summarize the latest AI developments"
4. Click "Submit Job"
5. You should receive a job ID
6. Switch to the "Pending" tab to see your job

### Test 5: Job Processing

1. Watch the "Pending" tab - jobs should update in real-time
2. Job status flow: `open` → `claimed` → `in_progress` → `completed`
3. Once completed, the job will appear in the "Completed" tab
4. You should see the result of the job processing

### Test 6: Dashboard Statistics

1. Navigate to the "Dashboard" page
2. Verify the following statistics update:
   - Active Jobs (running/queued/failed)
   - Monthly Spend
   - Jobs Completed
   - Avg Success Rate
3. Check the "Autonomous Agents" section shows all agents
4. Check the "Recent Jobs" table shows your submitted jobs

### Test 7: Marketplace

1. Navigate to the "Agents" page
2. You should see all available agents with:
   - Status (active/idle)
   - Success Rate
   - Pricing information
   - Capabilities

### Test 8: Profile Page

1. Navigate to your Profile
2. Verify account information displays correctly
3. Check credit balance
4. View active jobs

## Expected Behavior

### Job Submission Flow

1. **Frontend** → POST to `/submit_job` with task description
2. **Backend** → TundraAgent analyzes the request using Azure OpenAI
3. **Backend** → Determines which specialist agent to use
4. **Backend** → Creates job in MongoDB with status "open"
5. **Provider Agent Loop** → Agent claims the job (status → "claimed")
6. **Provider Agent Loop** → Agent processes job (status → "in_progress")
7. **Provider Agent Loop** → Agent completes job (status → "completed")
8. **Backend** → Updates credit balances
9. **Frontend** → Polls `/jobs` endpoint every 3 seconds
10. **Frontend** → Updates UI with new job status

### Real-Time Updates

- Jobs page refreshes every 3 seconds
- Dashboard refreshes every 5 seconds
- Marketplace refreshes every 5 seconds
- Profile refreshes every 5 seconds

### Credit System

- OrchestratorAgent starts with 1000 credits
- WebScraperAgent costs 15 credits per job
- SummarizerAgent costs 5 credits per job
- SentimentAgent costs 5 credits per job
- Credits are transferred when jobs complete successfully

## Troubleshooting

### Frontend cannot connect to backend

- Verify backend is running on http://localhost:8000
- Check `REACT_APP_BACKEND_URL` in `frontend/.env`
- Check browser console for CORS errors

### No jobs appearing

- Verify MongoDB connection in backend logs
- Check that MARKETPLACE_ENABLED=1 in backend .env
- Ensure provider agent loops are running (check backend logs)

### Jobs stuck in "open" status

- Check backend logs for errors
- Verify agent capabilities match task types
- Ensure MongoDB is accessible

### Authentication issues

- Verify Supabase credentials in frontend/.env
- Check Supabase project settings
- Ensure users are created in Supabase dashboard

### Azure OpenAI errors

- Verify AZURE_OPENAI_API_KEY is correct
- Check AZURE_DEPLOYMENT_NAME matches your deployment
- Ensure quota is not exceeded

## Backend API Endpoints

- `GET /` - Health check
- `GET /health` - Health check
- `GET /agents` - List all agents with balances
- `GET /jobs` - List all jobs (with optional status filter)
- `POST /submit_job` - Submit a new job
- `POST /execute` - Execute a job directly
- `POST /orchestrate` - Multi-agent orchestration
- `GET /jobs/{job_id}/score` - Get job scoring details
- `GET /marketplace/status` - Check marketplace status
- `POST /marketplace/reload` - Reload marketplace
- `GET /scoreboard` - Get agent performance stats

## Frontend Pages

- `/` or `/dashboard` - Main dashboard with stats and recent activity
- `/agents` - Marketplace of available agents
- `/jobs` - Job management (create, view, track)
- `/transactions` - Credit transaction history
- `/profile` - User profile and account info
- `/settings` - User settings and preferences

## Success Indicators

- Backend logs show "Marketplace online"
- Frontend loads without errors
- Agents appear in the marketplace
- Jobs can be submitted successfully
- Jobs progress through statuses: open → claimed → in_progress → completed
- Completed jobs show results
- Credit balances update correctly
- Dashboard statistics are accurate

## Common Issues and Solutions

1. **Port already in use**
   - Change port in backend: `uvicorn main:app --reload --port 8001`
   - Update REACT_APP_BACKEND_URL in frontend/.env

2. **MongoDB connection timeout**
   - Check MongoDB Atlas IP whitelist
   - Verify MONGO_URI is correct
   - Ensure network connectivity

3. **React build errors**
   - Delete node_modules and package-lock.json
   - Run `npm install` again
   - Clear npm cache: `npm cache clean --force`

4. **Python dependency issues**
   - Ensure virtual environment is activated
   - Update pip: `python -m pip install --upgrade pip`
   - Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## Next Steps

After successful integration testing:

1. Monitor job completion times
2. Track credit balance changes
3. Test error scenarios (invalid tasks, network issues)
4. Test with multiple concurrent jobs
5. Verify data persistence across restarts
