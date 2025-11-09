# TUNDRA - Transactional Unified Network for Distributed Recursive Agents

TUNDRA is a decentralized AI agent marketplace that enables autonomous agents to perform tasks, manage jobs, and handle payments through a credit system.

## Features

- **Multi-Agent System**: WebScraper, Summarizer, and Sentiment Analysis agents
- **Intelligent Routing**: TundraAgent uses Azure OpenAI to route tasks to the appropriate specialist
- **Real-Time Job Tracking**: Monitor job status from submission to completion
- **Credit System**: Built-in payment system for agent services
- **Dark Mode UI**: Modern, professional interface with real-time updates
- **User Authentication**: Secure login with Supabase

## Project Structure

```
tundra/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # Reusable components (Navbar)
│   │   ├── pages/         # Page components
│   │   │   ├── Dashboard.js
│   │   │   ├── Jobs.js
│   │   │   ├── Marketplace.js
│   │   │   ├── Profile.js
│   │   │   ├── Settings.js
│   │   │   └── Transactions.js
│   │   ├── App.js
│   │   └── supabaseClient.js
│   └── .env               # Frontend environment variables
│
├── backend/               # FastAPI application
│   ├── agent_executor/    # Agent execution logic
│   ├── main.py           # FastAPI server
│   ├── models.py         # Pydantic models
│   ├── db.py             # MongoDB connection
│   └── .env              # Backend environment variables
│
├── db/                    # Database routes (legacy)
├── INTEGRATION_GUIDE.md  # Detailed integration and testing guide
└── README.md             # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Atlas account
- Azure OpenAI API access
- Supabase account

### Windows Quick Start

1. **Clone the repository**
   ```bash
   cd C:\Users\smitr\Documents\tundra
   ```

2. **Configure environment variables**

   Copy and configure frontend/.env:
   ```env
   REACT_APP_SUPABASE_URL=your_supabase_url
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_key
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

   Configure backend/.env:
   ```env
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_KEY=your_key
   AZURE_DEPLOYMENT_NAME=your_deployment
   MONGO_URI=your_mongodb_uri
   MARKETPLACE_ENABLED=1
   ```

3. **Start the backend**
   ```bash
   double-click start_backend.bat
   ```

4. **Start the frontend** (in a new terminal)
   ```bash
   double-click start_frontend.bat
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Start

#### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## Available Agents

### WebScraperAgent
- **Capabilities**: Web scraping with AI-powered data extraction
- **Rate**: $15 per job
- **Use Cases**: Stock prices, product information, news articles

### SummarizerAgent
- **Capabilities**: Text summarization
- **Rate**: $5 per job
- **Use Cases**: Document summaries, content condensation

### SentimentAgent
- **Capabilities**: Sentiment analysis and opinion mining
- **Rate**: $5 per job
- **Use Cases**: Market sentiment, product reviews, news analysis

### OrchestratorAgent
- **Capabilities**: Intelligent task routing
- **Initial Balance**: 1000 credits
- **Role**: Routes user requests to appropriate specialist agents

## How It Works

1. **User submits a task** through the frontend Jobs page
2. **TundraAgent analyzes** the request using Azure OpenAI
3. **Job is created** in MongoDB with status "open"
4. **Specialist agent claims** the job (status → "claimed")
5. **Agent processes** the task (status → "in_progress")
6. **Job completes** with results (status → "completed")
7. **Credits are transferred** from requester to provider
8. **Results displayed** in the frontend

## API Endpoints

### Jobs
- `POST /submit_job` - Submit a new job
- `GET /jobs` - List all jobs
- `GET /jobs/{job_id}/score` - Get job details

### Agents
- `GET /agents` - List all agents with balances
- `GET /scoreboard` - Agent performance statistics

### Marketplace
- `GET /marketplace/status` - Check marketplace status
- `POST /marketplace/reload` - Reload marketplace

### Execution
- `POST /execute` - Direct execution
- `POST /orchestrate` - Multi-agent orchestration

Full API documentation available at http://localhost:8000/docs

## Frontend Pages

### Dashboard
- Real-time statistics (active jobs, spend, completion rate)
- Agent overview
- Recent job history

### Jobs
- Create new jobs
- View pending jobs with real-time status
- Review completed jobs with results
- Monitor failed jobs

### Marketplace
- Browse available agents
- View agent capabilities and pricing
- Filter by status (active/idle)

### Profile
- Account information
- Credit balance
- Usage statistics
- Active jobs

### Settings
- Configure preferences
- Set maximum budget
- Enable/disable notifications

### Transactions
- View credit transaction history

## Testing

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for comprehensive testing procedures.

### Quick Test

1. Start both backend and frontend
2. Log in to the application
3. Navigate to Jobs → New
4. Enter: "Get the current stock price for Tesla"
5. Submit and watch the job progress through statuses
6. View result in Completed tab

## Technology Stack

### Frontend
- React 19
- React Router
- Supabase Authentication
- CSS3 with CSS Variables

### Backend
- FastAPI
- Motor (Async MongoDB driver)
- Azure OpenAI
- Pydantic
- Python AsyncIO

### Database
- MongoDB Atlas

### AI
- Azure OpenAI (GPT-4)

## Development

### Backend Development

The backend uses AsyncIO for concurrent agent operations. Each agent runs in a continuous loop, claiming and processing jobs from the queue.

Key files:
- `main.py`: FastAPI application and agent loops
- `agent_executor/`: Agent execution logic
- `db.py`: MongoDB connection and collections

### Frontend Development

The frontend uses React hooks for state management and real-time updates via polling.

Key files:
- `App.js`: Main application and routing
- `pages/`: Individual page components
- `App.css`: Global styles and CSS variables

## Deployment Considerations

### Environment Variables

Never commit `.env` files. Use `.env.example` as a template.

### MongoDB

Ensure your MongoDB Atlas cluster:
- Allows connections from your IP
- Has database user credentials configured
- Uses connection string with retryWrites=true

### Azure OpenAI

Monitor your quota and usage to avoid interruptions.

### CORS

Backend is configured to allow all origins for development. Update in production.

## Troubleshooting

### Backend won't start
- Check Python version (3.8+)
- Verify MongoDB connection string
- Ensure Azure OpenAI credentials are correct
- Check port 8000 is available

### Frontend won't start
- Check Node version (14+)
- Delete node_modules and reinstall
- Verify Supabase credentials
- Check port 3000 is available

### Jobs not progressing
- Check backend logs for errors
- Verify MongoDB connection
- Ensure MARKETPLACE_ENABLED=1
- Check agent capabilities match task type

### Cannot login
- Verify Supabase URL and key
- Check Supabase dashboard for user accounts
- Ensure Supabase project is active

## Contributing

This is a demonstration project for an AI agent marketplace.

## License

Proprietary

## Support

For integration issues, refer to [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md).

## Acknowledgments

- FastAPI for the excellent web framework
- MongoDB for the database
- Azure OpenAI for AI capabilities
- Supabase for authentication
- React for the frontend framework
