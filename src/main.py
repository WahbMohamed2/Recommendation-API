from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from model import RecommendationRequest, RecommendationResponse
from recommendation_service import RecommendationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Question Recommendation API",
    description="API for generating personalized question recommendations",
    version="1.0.0",
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the recommendation service
recommendation_service = RecommendationService()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Question Recommendation API is running",
        "status": "healthy",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "recommendation-service",
        "timestamp": "2025-07-29",  # In production, use actual timestamp
    }


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_questions(request: RecommendationRequest) -> RecommendationResponse:
    """
    Generate question recommendations for a user

    This endpoint takes user information including their available topics,
    progress history, and desired number of questions, then returns
    personalized recommendations distributed across topics and difficulty levels.

    Args:
        request: RecommendationRequest containing user data and preferences

    Returns:
        RecommendationResponse with recommended questions organized by topic and level

    Raises:
        HTTPException: If the request is invalid or processing fails
    """
    try:
        logger.info(f"Processing recommendation request for user {request.user_id}")
        logger.debug(
            f"Request details: {request.total_questions} questions across {len(request.user_topics)} topics"
        )

        # Validate request
        _validate_recommendation_request(request)

        # Generate recommendations using the service
        response = recommendation_service.generate_recommendations(request)

        logger.info(
            f"Generated {response.total_recommended} total recommendations for user {request.user_id}"
        )
        return response

    except ValueError as e:
        logger.error(f"Validation error for user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            f"Unexpected error processing request for user {request.user_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while processing recommendation",
        )


def _validate_recommendation_request(request: RecommendationRequest) -> None:
    """
    Validate the recommendation request for business logic constraints

    Args:
        request: The request to validate

    Raises:
        ValueError: If the request fails validation
    """
    if not request.user_topics:
        raise ValueError("At least one topic must be provided")

    if request.total_questions <= 0:
        raise ValueError("Total questions must be greater than 0")

    # Validate that each topic has at least one available level
    for topic in request.user_topics:
        if not topic.available:
            raise ValueError(
                f"Topic '{topic.topic}' must have at least one available level"
            )

        # Validate that there are questions available
        total_available = sum(level.count for level in topic.available)
        if total_available == 0:
            raise ValueError(f"Topic '{topic.topic}' has no available questions")

    logger.debug("Request validation passed")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Question Recommendation API server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
