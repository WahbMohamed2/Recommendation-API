from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# Input models
class LevelAvailability(BaseModel):
    """Represents available questions for a specific level"""

    level: int = Field(..., description="The difficulty level")
    count: int = Field(..., ge=0, description="Number of available questions")


class TopicAvailability(BaseModel):
    """Represents a topic with its available levels and question counts"""

    topic: str = Field(..., description="Name of the topic")
    available: List[LevelAvailability] = Field(
        ..., description="Available levels and their question counts"
    )


class LevelProgress(BaseModel):
    """Represents user's progress for a specific level"""

    level: int = Field(..., description="The difficulty level")
    solved: int = Field(..., ge=0, description="Number of questions solved")
    attempted: int = Field(..., ge=0, description="Number of questions attempted")

    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage"""
        return (self.solved / self.attempted * 100) if self.attempted > 0 else 0.0


class TopicProgress(BaseModel):
    """Represents user's progress for a specific topic"""

    topic: str = Field(..., description="Name of the topic")
    progress_by_level: List[LevelProgress] = Field(
        ...,
        alias="progressByLevel",
        description="Progress data for each level within this topic",
    )

    def get_level_progress(self, level: int) -> Optional[LevelProgress]:
        """Get progress data for a specific level"""
        return next((p for p in self.progress_by_level if p.level == level), None)


class RecommendationRequest(BaseModel):
    """Request model for question recommendations"""

    user_id: int = Field(
        ..., alias="userId", description="Unique identifier for the user"
    )
    total_questions: int = Field(
        ...,
        alias="totalQuestions",
        ge=1,
        description="Total number of questions to recommend",
    )
    user_topics: List[TopicAvailability] = Field(
        ..., alias="userTopics", description="Available topics and their levels"
    )
    user_progress: List[TopicProgress] = Field(
        ..., alias="userProgress", description="User's historical progress data"
    )


# Response models
class LevelRecommendation(BaseModel):
    """Represents recommended question count for a specific level"""

    level: int = Field(..., description="The difficulty level")
    count: int = Field(..., ge=0, description="Number of questions recommended")


class TopicRecommendation(BaseModel):
    """Represents recommendations for a specific topic"""

    name: str = Field(..., description="Name of the topic")
    recommendations: List[LevelRecommendation] = Field(
        ..., description="Recommendations for each level"
    )

    @property
    def total_recommended(self) -> int:
        """Get total number of questions recommended for this topic"""
        return sum(rec.count for rec in self.recommendations)


class RecommendationResponse(BaseModel):
    """Response model for question recommendations"""

    topics: List[TopicRecommendation] = Field(
        ..., description="Recommendations organized by topic"
    )

    @property
    def total_recommended(self) -> int:
        """Get total number of questions recommended across all topics"""
        return sum(topic.total_recommended for topic in self.topics)
