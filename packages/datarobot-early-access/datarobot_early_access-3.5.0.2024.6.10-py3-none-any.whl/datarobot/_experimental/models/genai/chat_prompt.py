#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from mypy_extensions import TypedDict
import trafaret as t

from datarobot._experimental.models.enums import FeedbackSentiment
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.models.genai.chat_prompt import (  # noqa: F401; pylint: disable=unused-import
    Citation,
    citation_trafaret,
    confidence_scores_trafaret,
    ConfidenceScores,
)
from datarobot.models.genai.chat_prompt import (  # noqa: F401; pylint: disable=unused-import
    vector_database_settings_trafaret,
)
from datarobot.models.genai.chat_prompt import ChatPrompt as BaseChatPrompt
from datarobot.models.genai.chat_prompt import ResultMetadata as BaseResultMetadata


class FeedbackMetadataDict(TypedDict):
    feedback: FeedbackSentiment


class MetricMetadataDict(TypedDict):
    name: str
    value: Any
    formatted_value: Optional[str]
    sidecar_model_metric_validation_id: Optional[str]
    custom_model_id: Optional[str]
    evaluation_dataset_configuration_id: Optional[str]
    cost_configuration_id: Optional[str]


feedback_metadata_trafaret = t.Dict(
    {t.Key("feedback"): t.Enum(*enum_to_list(FeedbackSentiment))}
).ignore_extra("*")


metric_metadata_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("value"): t.Any,
        t.Key("formatted_value", optional=True): t.Or(t.String, t.Null),
        t.Key("sidecar_model_metric_validation_id", optional=True): t.Or(t.String, t.Null),
        t.Key("custom_model_id", optional=True): t.Or(t.String, t.Null),
        t.Key("evaluation_dataset_configuration_id", optional=True): t.Or(t.String, t.Null),
        t.Key("cost_configuration_id", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")


feedback_result_trafaret = t.Dict(
    {
        t.Key("positive_user_ids"): t.List(t.String),
        t.Key("negative_user_ids"): t.List(t.String),
    }
)


result_metadata_trafaret = t.Dict(
    {
        t.Key("cost", optional=True): t.Or(t.Float, t.Null),
        t.Key("output_token_count"): t.Int,
        t.Key("input_token_count"): t.Int,
        t.Key("total_token_count"): t.Int,
        t.Key("estimated_docs_token_count"): t.Int,
        t.Key("latency_milliseconds"): t.Int,
        t.Key("error_message", optional=True): t.Or(t.String, t.Null),
        t.Key("feedback_result"): feedback_result_trafaret,
        t.Key("metrics"): t.List(metric_metadata_trafaret),
        t.Key("final_prompt"): t.Or(
            t.String, t.Dict().allow_extra("*"), t.List(t.Dict().allow_extra("*")), t.Null
        ),
    }
).ignore_extra("*")


chat_prompt_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("text"): t.String,
        t.Key("llm_blueprint_id"): t.String,
        t.Key("llm_id"): t.String,
        t.Key("llm_settings", optional=True): t.Or(t.Dict().allow_extra("*"), t.Null),
        t.Key("creation_date"): t.String,
        t.Key("creation_user_id"): t.String,
        t.Key("vector_database_id", optional=True): t.Or(t.String, t.Null),
        t.Key("vector_database_settings", optional=True): t.Or(
            vector_database_settings_trafaret, t.Null
        ),
        t.Key("result_metadata", optional=True): t.Or(result_metadata_trafaret, t.Null),
        t.Key("result_text", optional=True): t.Or(t.String, t.Null),
        t.Key("confidence_scores", optional=True): t.Or(confidence_scores_trafaret, t.Null),
        t.Key("citations"): t.List(citation_trafaret),
        t.Key("execution_status"): t.String,
        t.Key("chat_id", optional=True): t.Or(t.String, t.Null),
        t.Key("chat_context_id", optional=True): t.Or(t.String, t.Null),
        t.Key("chat_prompt_ids_included_in_history", optional=True): t.Or(t.List(t.String), t.Null),
    }
).ignore_extra("*")


class FeedbackMetadata(APIObject):
    """
    Metadata for feedback associated with a chat prompt.

    Attributes
    ----------
    feedback : FeedbackSentiment
        The sentiment of the feedback.
    """

    _converter = feedback_metadata_trafaret

    def __init__(self, feedback: FeedbackSentiment):
        self.feedback = feedback

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(feedback={self.feedback})"

    def to_dict(self) -> FeedbackMetadataDict:
        return {"feedback": self.feedback}


class FeedbackResult(APIObject):
    """
    Feedback associated with a chat prompt.

    Attributes
    ----------
    positive_user_ids : List[str]
        The IDs of the users providing positive feedback.
    negative_user_ids : List[str]
        The IDs of the users providing negative feedback.
    """

    _converter = feedback_result_trafaret

    def __init__(self, positive_user_ids: List[str], negative_user_ids: List[str]):
        self.positive_user_ids = positive_user_ids
        self.negative_user_ids = negative_user_ids

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class MetricMetadata(APIObject):
    """
    Metadata for the custom metrics associated with a chat prompt.

    Attributes
    ----------
    name : str
        The name of the metric.
    value : Any
        The value of the metric.
    formatted_value : Optional[str], optional
        The formatted value of the metric, if any.
    sidecar_model_metric_validation_id : Optional[str], optional
        The ID of the sidecar model implementing the metric, if any.
    custom_model_id : Optional[str], optional
        The ID of the custom model implementing the metric, if any.
    evaluation_dataset_configuration_id : Optional[str], optional
        The ID of the evaluation dataset configuration associated with the metric, if any.
    cost_configuration_id : Optional[str], optional
        The ID of the cost configuration associated with the metric, if any.
    """

    _converter = metric_metadata_trafaret

    def __init__(
        self,
        name: str,
        value: Any,
        formatted_value: Optional[str] = None,
        sidecar_model_metric_validation_id: Optional[str] = None,
        custom_model_id: Optional[str] = None,
        evaluation_dataset_configuration_id: Optional[str] = None,
        cost_configuration_id: Optional[str] = None,
    ):
        self.name = name
        self.value = value
        self.formatted_value = formatted_value
        self.sidecar_model_metric_validation_id = sidecar_model_metric_validation_id
        self.custom_model_id = custom_model_id
        self.evaluation_dataset_configuration_id = evaluation_dataset_configuration_id
        self.cost_configuration_id = cost_configuration_id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name}, "
            f"value={self.value}, "
            f"formatted_value={self.formatted_value})"
        )

    def to_dict(self) -> MetricMetadataDict:
        return {
            "name": self.name,
            "value": self.value,
            "formatted_value": self.formatted_value,
            "sidecar_model_metric_validation_id": self.sidecar_model_metric_validation_id,
            "custom_model_id": self.custom_model_id,
            "evaluation_dataset_configuration_id": self.evaluation_dataset_configuration_id,
            "cost_configuration_id": self.cost_configuration_id,
        }


class ResultMetadata(BaseResultMetadata):
    """
    Metadata for the result of a chat prompt submission.

    Attributes
    ----------
    output_token_count : int
        The number of tokens in the output.
    input_token_count : int
        The number of tokens in the input. This includes the chat history and documents
        retrieved from a vector database, if any.
    total_token_count : int
        The total number of tokens processed.
    estimated_docs_token_count : int
        The estimated number of tokens from the documents retrieved from a vector database, if any.
    latency_milliseconds : int
        The latency of the chat prompt submission in milliseconds.
    feedback_result : FeedbackResult
        The lists of user_ids providing positive and negative feedback.
    metrics : MetricMetadata
        The evaluation metrics for this prompt.
    final_prompt : Optional[Union[str, dict]], optional
        Representation of the final prompt sent to the LLM.
    error_message : str or None, optional
        The error message from the LLM response.
    cost : float or None, optional
        The cost of the chat prompt submission.
    """

    _converter = result_metadata_trafaret

    def __init__(
        self,
        output_token_count: int,
        input_token_count: int,
        total_token_count: int,
        estimated_docs_token_count: int,
        latency_milliseconds: int,
        feedback_result: Dict[str, Any],
        metrics: List[Dict[str, Any]],
        final_prompt: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        error_message: Optional[str] = None,
        cost: Optional[float] = None,
    ):
        super().__init__(
            output_token_count,
            input_token_count,
            total_token_count,
            estimated_docs_token_count,
            latency_milliseconds,
            error_message,
            cost,
        )
        self.feedback_result = FeedbackResult.from_server_data(feedback_result)
        self.metrics = [
            MetricMetadata.from_server_data(metric_metadata) for metric_metadata in metrics
        ]
        self.final_prompt = final_prompt


class ChatPrompt(BaseChatPrompt):
    """
    Metadata for a DataRobot GenAI chat prompt.

    Attributes
    ----------
    id : str
        Chat prompt ID.
    text : str
        The prompt text.
    llm_blueprint_id : str
        ID of the LLM blueprint associated with the chat prompt.
    llm_id : str
        ID of the LLM type. This must be one of the IDs returned by `LLMDefinition.list`
        for this user.
    llm_settings : dict or None
        The LLM settings for the LLM blueprint. The specific keys allowed and the
        constraints on the values are defined in the response from `LLMDefinition.list`,
        but this typically has dict fields. Either:
        - system_prompt - The system prompt that influences the LLM responses.
        - max_completion_length - The maximum number of tokens in the completion.
        - temperature - Controls the variability in the LLM response.
        - top_p - Sets whether the model considers next tokens with top_p probability mass.
        or
        - system_prompt - The system prompt that influences the LLM responses.
        - validation_id - The ID of the external model LLM validation.
        - external_llm_context_size - The external LLM's context size, in tokens,
        for external model-based LLM blueprints.
    creation_date : str
        The date the chat prompt was created.
    creation_user_id : str
        ID of the creating user.
    vector_database_id : str or None
        ID of the vector database associated with the LLM blueprint, if any.
    vector_database_settings : VectorDatabaseSettings or None
        The settings for the vector database associated with the LLM blueprint, if any.
    result_metadata : ResultMetadata or None
        Metadata for the result of the chat prompt submission.
    result_text: str or None
        The result text from the chat prompt submission.
    confidence_scores: ConfidenceScores or None
        The confidence scores if there is a vector database associated with the chat prompt.
    citations: list[Citation]
        List of citations from text retrieved from the vector database, if any.
    execution_status: str
        The execution status of the chat prompt.
    chat_id: Optional[str]
        ID of the chat associated with the chat prompt.
    chat_context_id: Optional[str]
        The ID of the chat context for the chat prompt.
    chat_prompt_ids_included_in_history: Optional[list[str]]
        The IDs of the chat prompts included in the chat history for this chat prompt.
    """

    _converter = chat_prompt_trafaret

    def __init__(
        self,
        id: str,
        text: str,
        llm_blueprint_id: str,
        llm_id: str,
        creation_date: str,
        creation_user_id: str,
        citations: List[Dict[str, Any]],
        execution_status: str,
        llm_settings: Optional[Dict[str, Any]] = None,
        vector_database_id: Optional[str] = None,
        vector_database_settings: Optional[Dict[str, Any]] = None,
        result_metadata: Optional[Dict[str, Any]] = None,
        result_text: Optional[str] = None,
        confidence_scores: Optional[Dict[str, float]] = None,
        chat_id: Optional[str] = None,
        chat_context_id: Optional[str] = None,
        chat_prompt_ids_included_in_history: Optional[list[str]] = None,
    ):
        super().__init__(
            id,
            text,
            llm_blueprint_id,
            llm_id,
            creation_date,
            creation_user_id,
            citations,
            execution_status,
            llm_settings,
            vector_database_id,
            vector_database_settings,
            result_metadata,
            result_text,
            confidence_scores,
            chat_id,
            chat_context_id,
            chat_prompt_ids_included_in_history,
        )
        self.result_metadata = (
            ResultMetadata.from_server_data(result_metadata) if result_metadata else None
        )

    def update(
        self,
        custom_metrics: Optional[list[MetricMetadata]] = None,
        feedback_metadata: Optional[FeedbackMetadata] = None,
    ) -> ChatPrompt:
        """
        Update the chat prompt.

        Parameters
        ----------
        custom_metrics : Optional[list[MetricMetadata]], optional
            The new custom metrics to add to the chat prompt.
        feedback_metadata: Optional[FeedbackMetadata], optional
            The new feedback to add to the chat prompt.

        Returns
        -------
        chat_prompt : ChatPrompt
            The updated chat prompt.
        """
        payload = {
            "custom_metrics": [metadata.to_dict() for metadata in custom_metrics]
            if custom_metrics
            else None,
            "feedback_metadata": feedback_metadata.to_dict() if feedback_metadata else None,
        }
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        r_data = self._client.patch(url, data=payload)
        return self.from_server_data(r_data.json())
