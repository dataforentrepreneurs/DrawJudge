# DrawJudge 🎨⚖️

DrawJudge is an AI-powered drawing party game where players are given a prompt, draw it on a shared canvas, and an AI judge scores their drawing based on accuracy, creativity, and style!

## 🚀 Tech Stack

- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, WebSockets
- **AI Integration**: Google Generative AI (Gemini Vision)

## 🛠️ Project Structure

- `/frontend` - The React application where players draw and interact in real-time.
- `/backend` - The FastAPI server that handles game state, WebSocket connections, and communicates with the AI judge.

## 🏃‍♂️ How to Run Locally

### 1. Start the Backend

Navigate to the backend directory, set up your virtual environment, and run the server:

```bash
cd backend

# Create a virtual environment (depending on your OS)
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
fastapi dev main.py
```

The backend will run at `http://localhost:8000`.

### 2. Start the Frontend

Open a new terminal, navigate to the frontend directory, install dependencies, and start the Vite dev server:

```bash
cd frontend

# Install dependencies
npm install

# Run the frontend server
npm run dev
```

The frontend will typically run at `http://localhost:5173`. Open this URL in your browser to start playing!

## 🎮 How to Play

1. A player creates a game room and shares the Room Code (or QR code) with friends.
2. Friends join the room using their mobile devices or browsers.
3. The game gives everyone a fun prompt to draw.
4. Players draw their interpretation on the canvas and submit it before time runs out.
5. The AI Judge analyzes all submissions and awards points!

## 🤖 AI Setup

Currently, the game may use a mock AI judge for testing. To use the real Google Generative AI judge, ensure you have your `GEMINI_API_KEY` configured in your backend environment variables.
