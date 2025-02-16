l# 🚀 LLM-based Automation Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

✨ **Automate Tasks with Natural Language Processing**

This project implements an intelligent automation agent that processes plain-English task descriptions and executes multi-step operations accordingly. The agent uses a combination of file operations, external tool invocations, and simulated LLM calls to process tasks defined by DataWorks Solutions' operations and business teams.


## 📂 Project Structure

```bash
project-root/
├── Data
├── LICENSE
├── Dockerfile
├── README.md
├── requirements.txt
├── app.py
├── agent.py
├── tasks.py
└── llm_client.py
```


| File/Folder         | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `LICENSE`           | MIT License for the project                                                |
| `Dockerfile`        | Docker configuration to build and run the application                     |
| `README.md`         | Project documentation (you're reading it!)                                  |
| `requirements.txt`  | Python dependencies                                                         |
| `app.py`            | Main Flask application exposing the `/run` and `/read` endpoints           |
| `agent.py`          | Delegates task execution to the task handler                                |
| `tasks.py`          | Contains implementations for operations tasks (A1–A10) and business tasks (B3–B10) |
| `llm_client.py`     | Simulates LLM (GPT-4o-Mini) interactions for text and image tasks          |


## 🌐 API Endpoints

### POST `/run?task=<task description>`
Executes the specified task. The task is provided as a plain-English description.

**Example:**
```bash
"Count the number of Wednesdays in /data/dates.txt and write the number to /data/dates-wednesdays.txt"
```

**Responses:**
| Status Code | Description                          |
|-------------|--------------------------------------|
| 200 OK      | Success with JSON message            |
| 400         | Bad Request (invalid task description)|
| 500         | Internal Server Error                |

### GET `/read?path=<file path>`
Reads the content of the specified file (only files under `/data` are accessible).

**Responses:**
| Status Code | Description                          |
|-------------|--------------------------------------|
| 200 OK      | File content as plain text          |
| 404         | Not Found (file doesn't exist)      |
| 403         | Forbidden (access outside /data)     |


## 🚦 Getting Started

### Prerequisites

- 🐳 Docker (or Podman)
- 🐍 Python 3.9+ (for local development)

### Environment Variables

Create a `.env` file with the following content:

```bash
AIPROXY_TOKEN=your_actual_token
USER_EMAIL=your_email@example.com
```

> **Note:** For security reasons, never commit your `.env` file to version control!


### 🐳 Docker Setup

1. **Build the Docker Image:**
   ```bash
   docker build -t your-username/your-repo .
   ```

2. **Run the Container:**
   - Using Docker:
     ```bash
     docker run --rm -p 8000:8000 --env-file .env your-username/your-repo
     ```
   - Using Podman:
     ```bash
     podman run --rm -p 8000:8000 --env-file .env your-username/your-repo
     ```


### 🧪 Testing the API

1. **Execute a Task:**
   ```bash
   curl -X POST "http://localhost:8000/run?task=Count the number of Wednesdays in /data/dates.txt and write to /data/dates-wednesdays.txt"
   ```

2. **Verify Output:**
   ```bash
   curl "http://localhost:8000/read?path=/data/dates-wednesdays.txt"
   ```

3. **Example Output:**
   ```bash
   "Number of Wednesdays: 5"
   ```


### 💡 Notes & Best Practices

- 🔒 **Security:** The agent restricts file access to the `/data` directory for security
- 🤖 **LLM Integration:** Simulated LLM responses in `llm_client.py` can be replaced with actual API calls
- 🧩 **Modular Design:** Task handlers are modular - easily add new handlers or extend existing ones
- 📁 **Data Management:** Keep all input/output files in the `/data` directory
- 🚨 **Error Handling:** Check API responses for status codes and error messages


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Your Name/Organization] | [Contribute](#) | [Report Issues](#)


---

## Proof of Functionality
The project was tested with sample dates in /data/dates.txt. The task successfully counted 5 Wednesdays and wrote the result to /data/dates-wednesdays.txt, confirming correct functionality.
