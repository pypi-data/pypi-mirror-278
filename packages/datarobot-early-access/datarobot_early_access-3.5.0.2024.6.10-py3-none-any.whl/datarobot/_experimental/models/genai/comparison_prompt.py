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

from typing import Any, List, Optional, Union

from mypy_extensions import TypedDict
import trafaret as t

from datarobot._experimental.models.genai.chat_prompt import (
    feedback_metadata_trafaret,
    FeedbackMetadata,
    FeedbackMetadataDict,
)
from datarobot.models.api_object import APIObject
from datarobot.models.genai.comparison_prompt import ComparisonPrompt as BaseComparisonPrompt
from datarobot.models.genai.comparison_prompt import _get_genai_entity_id
from datarobot.models.genai.llm_blueprint import LLMBlueprint
from datarobot.utils.waiters import wait_for_async_resolution


class FeedbackResultDict(TypedDict):
    comparison_prompt_result_id: str
    feedback_metadata: FeedbackMetadataDict


feedback_result_trafaret = t.Dict(
    {
        t.Key("comparison_prompt_result_id"): t.String,
        t.Key("feedback_metadata"): feedback_metadata_trafaret,
    }
).ignore_extra("*")


class FeedbackResult(APIObject):
    """
    Feedback associated with a comparison prompt result.

    Attributes
    ----------
    comparison_prompt_result_id : str
        The ID of the comparison prompt result associated with the feedback.
    feedback_metadata : FeedbackMetadata
        The metadata for the feedback.
    """

    _converter = feedback_result_trafaret

    def __init__(self, comparison_prompt_result_id: str, feedback_metadata: FeedbackMetadata):
        self.comparison_prompt_result_id = comparison_prompt_result_id
        self.feedback_metadata = feedback_metadata

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(comparison_prompt_result_id={self.comparison_prompt_result_id},"
            f"feedback_metadata={self.feedback_metadata})"
        )

    def to_dict(self) -> FeedbackResultDict:
        return {
            "comparison_prompt_result_id": self.comparison_prompt_result_id,
            "feedback_metadata": self.feedback_metadata.to_dict(),
        }


class ComparisonPrompt(BaseComparisonPrompt):
    """
    Metadata for a DataRobot GenAI comparison prompt.

    Attributes
    ----------
    id : str
        Comparison prompt ID.
    text : str
        The prompt text.
    results : list[ComparisonPromptResult]
        The list of results for individual LLM blueprints that are part of the comparison prompt.
    creation_date : str
        The date when the playground was created.
    creation_user_id : str
        ID of the creating user.
    comparison_chat_id : str
        The ID of the comparison chat this comparison prompt is associated with.
    """

    def update(
        self,
        additional_llm_blueprints: Optional[List[Union[LLMBlueprint, str]]] = None,
        wait_for_completion: bool = False,
        feedback_result: Optional[FeedbackResult] = None,
        **kwargs: Any,
    ) -> ComparisonPrompt:
        """
        Update the comparison prompt.

        Parameters
        ----------
        additional_llm_blueprints : list[LLMBlueprint or str]
            The additional LLM blueprints you want to submit the comparison prompt.

        Returns
        -------
        comparison_prompt : ComparisonPrompt
            The updated comparison prompt.
        """
        payload = {
            "additionalLLMBlueprintIds": [
                _get_genai_entity_id(bp) for bp in additional_llm_blueprints
            ]
            if additional_llm_blueprints
            else None,
            "feedbackResult": feedback_result.to_dict() if feedback_result else None,
        }
        url = f"{self._client.domain}/{self._path}/{_get_genai_entity_id(self.id)}/"
        r_data = self._client.patch(url, data=payload)
        if wait_for_completion and additional_llm_blueprints:
            # If no additional_llm_blueprints then we get no location header
            location = wait_for_async_resolution(self._client, r_data.headers["Location"])
            return self.from_location(location)
        else:
            # Update route returns empty string so we need to GET here
            r_data = self._client.get(url)
            return self.from_server_data(r_data.json())
