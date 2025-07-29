# Question Recommendation API

A high-performance, scalable REST API built with FastAPI that provides intelligent question recommendations for personalized learning experiences. The system dynamically distributes practice questions across topics and difficulty levels based on user progress and question availability.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [License](#-license)

## ⭐ Features

- **Intelligent Question Distribution**: Dynamically allocates questions across topics and difficulty levels
- **Scalable Architecture**: Modular design with service layer separation and strategy pattern
- **Progress-Aware**: Ready for integration with user progress data for personalized recommendations
- **High Performance**: Built on FastAPI with async support and automatic validation
- **Comprehensive Validation**: Request validation with detailed error messages
- **Production Ready**: Includes logging, health checks, CORS support, and error handling
- **Extensible**: Plugin architecture for custom distribution strategies
- **Type Safe**: Full type annotations with Pydantic models

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   FastAPI       │    │   Service Layer  │    │   Strategy Pattern  │
│   (API Layer)   │───▶│   (Business      │───▶│   (Distribution     │
│                 │    │    Logic)        │    │    Algorithms)      │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Pydantic      │    │   Validation     │    │   Logging &         │
│   (Data Models) │    │   & Error        │    │   Monitoring        │
│                 │    │   Handling       │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/question-recommendation-api.git
   cd question-recommendation-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Linux/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Verify installation**
   
   Open your browser and navigate to:
   - API: http://127.0.0.1:8000
   - Interactive API Documentation: http://127.0.0.1:8000/docs
   - Alternative API Documentation: http://127.0.0.1:8000/redoc

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API status |
| GET | `/health` | Detailed health check |
| POST | `/recommend` | Generate question recommendations |

### POST `/recommend`

Generate personalized question recommendations based on user data and preferences.

#### Request Body

```json
{
  "userId": 123,
  "totalQuestions": 10,
  "userTopics": [
    {
      "topic": "Math",
      "available": [
        { "level": 1, "count": 20 },
        { "level": 2, "count": 15 },
        { "level": 3, "count": 10 }
      ]
    },
    {
      "topic": "Physics",
      "available": [
        { "level": 1, "count": 25 },
        { "level": 2, "count": 12 }
      ]
    }
  ],
  "userProgress": [
    {
      "topic": "Math",
      "progressByLevel": [
        { "level": 1, "solved": 8, "attempted": 10 },
        { "level": 2, "solved": 3, "attempted": 5 }
      ]
    }
  ]
}
```

#### Response

```json
{
  "topics": [
    {
      "name": "Math",
      "recommendations": [
        { "level": 1, "count": 2 },
        { "level": 2, "count": 2 },
        { "level": 3, "count": 1 }
      ]
    },
    {
      "name": "Physics",
      "recommendations": [
        { "level": 1, "count": 3 },
        { "level": 2, "count": 2 }
      ]
    }
  ]
}
```

#### Error Responses

- **400 Bad Request**: Invalid request data or validation errors
- **500 Internal Server Error**: Unexpected server errors

## 📁 Project Structure

```
question-recommendation-api/
├── main.py                     # FastAPI application entry point
├── model.py                    # Pydantic data models and schemas
├── recommendation_service.py   # Business logic and service layer
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                # Git ignore rules

```

### Core Components

- **`main.py`**: FastAPI application with route definitions, middleware, and error handling
- **`model.py`**: Pydantic models for request/response validation and data serialization
- **`recommendation_service.py`**: Business logic service with pluggable distribution strategies


### Production Considerations

- **Environment Variables**: Use environment variables for configuration
- **Database**: Integrate with your preferred database for persistence
- **Caching**: Add Redis or similar for caching recommendations
- **Monitoring**: Integrate with monitoring tools (Prometheus, Grafana)
- **Rate Limiting**: Implement rate limiting for production use
- **Authentication**: Add JWT or OAuth2 authentication

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive tests
- Update documentation for new features
- Use meaningful commit messages


##  Security

- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error messages without data leakage
- **CORS**: Configurable CORS settings
- **Type Safety**: Full type checking prevents common errors


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation library
- [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

---
