from typing import List, Dict
from model import (
    RecommendationRequest,
    RecommendationResponse,
    TopicRecommendation,
    LevelRecommendation,
    TopicAvailability,
    TopicProgress,
    LevelAvailability,
)


class RecommendationService:
    """Service class that handles the business logic for question recommendations"""

    def __init__(self):
        self.distribution_strategy = EvenDistributionStrategy()

    def generate_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        """
        Generate question recommendations based on the request

        Args:
            request: The recommendation request containing user data and preferences

        Returns:
            RecommendationResponse with recommended questions per topic and level
        """
        # Create a lookup for user progress by topic
        progress_lookup = self._create_progress_lookup(request.user_progress)

        # Generate recommendations for each topic
        topic_recommendations = []
        for topic in request.user_topics:
            topic_progress = progress_lookup.get(topic.topic)
            recommendation = self._recommend_for_topic(
                topic=topic,
                total_questions=request.total_questions,
                topic_progress=topic_progress,
                all_topics=request.user_topics,
            )
            topic_recommendations.append(recommendation)

        return RecommendationResponse(topics=topic_recommendations)

    def _create_progress_lookup(
        self, user_progress: List[TopicProgress]
    ) -> Dict[str, TopicProgress]:
        """Create a dictionary lookup for user progress by topic name"""
        return {progress.topic: progress for progress in user_progress}

    def _recommend_for_topic(
        self,
        topic: TopicAvailability,
        total_questions: int,
        topic_progress: TopicProgress = None,
        all_topics: List[TopicAvailability] = None,
    ) -> TopicRecommendation:
        """
        Generate recommendations for a single topic

        Args:
            topic: The topic to generate recommendations for
            total_questions: Total questions to distribute across all topics
            topic_progress: User's progress for this topic (optional)
            all_topics: All available topics (used for distribution calculation)

        Returns:
            TopicRecommendation for the given topic
        """
        # Calculate questions allocated to this topic
        topic_question_allocation = self._calculate_topic_allocation(
            topic, total_questions, all_topics or [topic]
        )

        # Distribute questions across levels within this topic
        level_recommendations = self.distribution_strategy.distribute_questions(
            available_levels=topic.available,
            total_questions=topic_question_allocation,
            topic_progress=topic_progress,
        )

        return TopicRecommendation(
            name=topic.topic, recommendations=level_recommendations
        )

    def _calculate_topic_allocation(
        self,
        current_topic: TopicAvailability,
        total_questions: int,
        all_topics: List[TopicAvailability],
    ) -> int:
        """
        Calculate how many questions should be allocated to the current topic

        Currently uses even distribution, but can be enhanced to consider:
        - User preferences
        - Historical performance
        - Topic difficulty
        """
        total_topics = len(all_topics)
        return total_questions // total_topics if total_topics > 0 else 0


class DistributionStrategy:
    """Abstract base class for question distribution strategies"""

    def distribute_questions(
        self,
        available_levels: List[LevelAvailability],
        total_questions: int,
        topic_progress: TopicProgress = None,
    ) -> List[LevelRecommendation]:
        """Distribute questions across levels according to the strategy"""
        raise NotImplementedError


class EvenDistributionStrategy(DistributionStrategy):
    """Strategy that distributes questions evenly across all available levels"""

    def distribute_questions(
        self,
        available_levels: List[LevelAvailability],
        total_questions: int,
        topic_progress: TopicProgress = None,
    ) -> List[LevelRecommendation]:
        """
        Distribute questions evenly across all available levels

        Args:
            available_levels: List of available levels with their question counts
            total_questions: Total questions to distribute
            topic_progress: User's progress for this topic (currently unused but ready for future enhancement)

        Returns:
            List of LevelRecommendation objects
        """
        if not available_levels:
            return []

        level_count = len(available_levels)
        base_questions_per_level = total_questions // level_count
        extra_questions = total_questions % level_count

        recommendations = []
        for i, level_data in enumerate(available_levels):
            # Distribute extra questions to first few levels
            questions_for_level = base_questions_per_level + (
                1 if i < extra_questions else 0
            )

            # Ensure we don't exceed available questions for this level
            recommended_count = min(questions_for_level, level_data.count)

            # Future enhancement: Consider user progress here
            # if topic_progress:
            #     level_progress = topic_progress.get_level_progress(level_data.level)
            #     recommended_count = self._adjust_for_progress(recommended_count, level_progress)

            recommendations.append(
                LevelRecommendation(level=level_data.level, count=recommended_count)
            )

        return recommendations


class ProgressAwareDistributionStrategy(DistributionStrategy):
    """
    Future strategy that considers user progress when distributing questions
    This is a placeholder for future enhancement
    """

    def distribute_questions(
        self,
        available_levels: List[LevelAvailability],
        total_questions: int,
        topic_progress: TopicProgress = None,
    ) -> List[LevelRecommendation]:
        """
        Distribute questions based on user's historical performance

        Future implementation could:
        - Prioritize levels where user has lower success rates
        - Avoid levels where user has already solved most questions
        - Consider recent performance trends
        """
        # For now, fall back to even distribution
        # TODO: Implement progress-aware logic
        even_strategy = EvenDistributionStrategy()
        return even_strategy.distribute_questions(
            available_levels, total_questions, topic_progress
        )
