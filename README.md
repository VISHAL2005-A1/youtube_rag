# 🎥 YouTube Playlist RAG Assistant – AI-Powered Lecture Q&A

A RAG-based AI application that lets users ask questions about YouTube lectures and get answers grounded in the lecture transcripts, along with the **relevant video and timestamp**.

🔗 **Live Demo:** [http://13.222.168.144:3000](http://13.222.168.144:3000)

![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_EC2-FF9900?logo=amazonaws&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

---

## 📑 Table of Contents

- [Tech Stack](#️-tech-stack)
- [Features](#-features)
- [How It Works](#️-how-it-works)
- [The Process](#️-the-process)
- [What I Learned](#-what-i-learned)
- [How Can It Be Improved?](#-how-can-it-be-improved)
- [Running the Project](#-running-the-project)
- [Running with Docker](#-running-with-docker)
- [Author](#-author)

---

## 🛠️ Tech Stack

| Category | Technologies |
| --- | --- |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS |
| **Backend** | Python, FastAPI |
| **AI** | Groq, Sentence Transformers |
| **Vector Database** | Qdrant |
| **Transcript Processing** | yt-dlp |
| **Deployment** | Docker, AWS EC2 |
| **CI/CD** | GitHub Actions, Docker Hub |

---

## ✨ Features

- **Ask Questions:** Ask questions related to the YouTube lectures.
- **Semantic Search:** Find relevant lecture content using vector search.
- **Grounded Answers:** Get answers based only on the lecture transcripts.
- **Video Reference:** Get the relevant lecture video for the answer.
- **Timestamp:** Find exactly where the topic is discussed in the lecture.
- **No Hallucination:** If the topic is not present in the lectures, the system does not make up an answer.
- **Multilingual Transcripts:** Supports transcript content in multiple languages.
- **Dockerized:** Run the complete application using Docker.
- **Cloud Deployment:** Deployed on AWS EC2.

---

## ⌨️ How It Works

1. **Question:** The user asks a question related to the playlist.
2. **Embedding:** The question is converted into a vector embedding.
3. **Search:** Qdrant searches for the most relevant transcript chunks.
4. **Context:** The relevant transcript content is sent to Groq.
5. **Answer:** Groq generates an answer using only the retrieved lecture content.
6. **Reference:** The application shows the relevant video and timestamp.

```
User Question → Embedding → Qdrant Search → Relevant Chunks → Groq LLM → Answer + Video + Timestamp
```

---

## ⚙️ The Process

I started by collecting the YouTube lecture transcripts and processing them into smaller chunks.

Next, I converted each chunk into embeddings using Sentence Transformers and stored the embeddings, along with video information and timestamps, in Qdrant.

When a user asks a question, the question is converted into an embedding and searched against the stored lecture embeddings. The most relevant chunks are then sent to Groq as context.

Finally, I built the React frontend, connected it with the FastAPI backend, containerized the application using Docker, and deployed it on AWS EC2 with GitHub Actions for CI/CD.

---

## 📚 What I Learned

This project helped me understand how a practical RAG application is built and deployed.

### 🧠 RAG & Embeddings
- Learned how to build a complete RAG pipeline.
- Worked with text embeddings and semantic search.
- Learned how to retrieve relevant information from large amounts of text.

### 🗄️ Qdrant
- Learned how to store and search vector embeddings.
- Worked with metadata such as video title, video ID, and timestamps.

### 🤖 Groq
- Integrated an LLM with retrieved context.
- Learned how to control responses using system prompts and context.

### 🎥 YouTube Transcripts
- Worked with transcript files and timestamp information.
- Connected transcript content with the original lecture videos.

### 🐳 Docker & AWS
- Containerized the frontend and backend.
- Deployed the application on AWS EC2.
- Used Docker Hub for storing images.

### 🔄 CI/CD
- Created a GitHub Actions workflow.
- Automated Docker image building and pushing.
- Automated deployment to the EC2 server.

---

## 🔧 How Can It Be Improved?

- [ ] Automatically fetch and process YouTube transcripts.
- [ ] Improve timestamp accuracy.
- [ ] Add hybrid keyword + vector search.
- [ ] Add streaming AI responses.
- [ ] Support multiple YouTube playlists.
- [ ] Add RAG evaluation and benchmarking.

---

## 🚀 Running the Project

To run this project in your local environment, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/VISHAL2005-A1/Rag_system.git
cd Rag_system
```

### 2. Set Up the Backend

Navigate to the backend:

```bash
cd backend
```

Install the required dependencies:

```bash
uv sync
```

Create a `.env` file inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=youtube_playlist_chunks
YOUTUBE_API_KEY=your_youtube_api_key
```

Start the backend:

```bash
uv run uvicorn main:app --reload
```

The backend will run at: `http://localhost:8000`

### 3. Set Up the Frontend

Open a new terminal and navigate to the frontend:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

The frontend will run at: `http://localhost:3000`

### 4. Add the Lecture Data

Place the YouTube lecture transcript `.vtt` files inside:

```
backend/transcripts/
```

Then run the project's transcript ingestion process to create embeddings and store them in Qdrant.

### 5. Open the Application

Open your browser and visit `http://localhost:3000`.

Now you can ask questions related to the lecture transcripts.

**Example questions:**

```
What is an LLM?
```

```
Where is RAG explained in the playlist?
```

If the topic exists in the lecture, the application provides the relevant video and timestamp.

---

## 🐳 Running with Docker

Run the complete application (frontend + backend) with a single command using Docker Compose.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A Qdrant instance (for example, a free [Qdrant Cloud](https://cloud.qdrant.io/) cluster)
- A [Groq API key](https://console.groq.com/)

Verify Docker is ready:

```bash
docker --version
docker compose version
```

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/VISHAL2005-A1/Rag_system.git
cd Rag_system
```

**2. Create the `.env` file** inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=youtube_playlist_chunks
YOUTUBE_API_KEY=your_youtube_api_key
```

**3. Add the lecture transcripts.** Place the `.vtt` files inside:

```
backend/transcripts/
```

**4. Build and start the containers** from the project root (where `docker-compose.yml` is located):

```bash
docker compose up --build
```

To run in the background, add the `-d` flag:

```bash
docker compose up --build -d
```

**5. Run the ingestion step** to create embeddings and store them in Qdrant:

```bash
docker compose exec backend python ingest.py
```

> This only needs to be done once, or again whenever you add new transcripts. The app cannot answer questions until the embeddings are stored in Qdrant.

**6. Open the application**

| Service | URL |
| --- | --- |
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### Useful Docker Commands

```bash
docker compose logs -f          # View live logs
docker compose ps               # List running containers
docker compose down             # Stop and remove containers
docker compose up --build       # Rebuild after code changes
```

### Troubleshooting

| Problem | Solution |
| --- | --- |
| **Port already in use** | Stop the process using port `3000` or `8000`, or change the port mapping in `docker-compose.yml`. |
| **Backend crashes on startup** | Check that the `.env` file exists inside `backend/` and all keys are set. View logs with `docker compose logs backend`. |
| **Frontend can't reach the backend** | Make sure the frontend API URL points to `http://localhost:8000` for local runs. |
| **Answers come back empty** | Ingestion hasn't been run, or `QDRANT_COLLECTION` doesn't match the collection you ingested into. |

> ⚠️ **Note:** Never commit your `.env` file or API keys to GitHub.

---

## 👨‍💻 Author

**Vishal Gautam**

- 🔗 LinkedIn: [Add your LinkedIn URL here](https://www.linkedin.com/in/your-profile)
- 🐙 GitHub: [VISHAL2005-A1](https://github.com/VISHAL2005-A1)
- 📧 Email: vishalgautam1118465@gmail.com

---

⭐ If you found this project useful, please consider giving it a star!
