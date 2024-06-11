from typing import Type

import pytest

from pydantic import BaseModel, Field

from typedllm import (
    LLMModel,
    LLMSession,
    LLMRequest,
    LLMUserMessage,
    request,
    async_request,
    create_tool_from_function,
    Tool
)
from typedllm.client import typed_request, async_tool_from_json_str, sync_tool_from_json_str


@pytest.mark.asyncio
async def test_basic_request(openai_key: str):
    model = LLMModel(
        name="gpt-4-0125-preview",
        api_key=openai_key,
    )
    session = LLMSession(
        model=model,
    )
    request = LLMRequest(
        message=LLMUserMessage(
            content="What year was New York City founded?",
        ),
        force_text_response=True
    )
    session, response = await async_request(session, request)
    assert response.message.content.index("1624") > -1


class CityFoundingInfo(Tool):
    """This represents a city and includes the year the city was founded."""
    year: int = Field(description="The year the city was founded.")
    city: str = Field(description="The name of the city.")


def get_city_founding_history(city_info: CityFoundingInfo) -> str:
    return (f"Historical weather for {city_info.city} since its founding in {city_info.year}. "
            f"The weather is very nice. Average 80 degrees F.")


def test_make_tool_from_function():
    Tool = create_tool_from_function(get_city_founding_history)
    assert Tool.__name__ == "get_city_founding_history"
    assert "city_info" in Tool.model_fields
    assert Tool.model_fields["city_info"].annotation == CityFoundingInfo


@pytest.mark.asyncio
async def test_basic_tools_request(openai_key: str):
    model = LLMModel(
        name="gpt-4",
        api_key=openai_key,
    )
    tool: Type[Tool] = create_tool_from_function(get_city_founding_history)
    session = LLMSession(
        model=model,
        tools=[tool]
    )
    request = LLMRequest(
        message=LLMUserMessage(
            content="What is the founding story of New York City?",
        ),
        required_tool=tool,
    )
    session, response = await async_request(session, request)
    assert session
    assert response
    assert response.tool_calls[0].tool.__class__.__name__ == "get_city_founding_history"
    assert response.tool_calls[0].tool.city_info.city.index("New York") > -1
    assert response.tool_calls[0].tool.city_info.year == 1624


@pytest.mark.asyncio
async def test_typed_request(openai_key: str, llmprompt):
    class Year(Tool):
        year: int = Field(description="The year of the city's founding")

    model = LLMModel(
        name="gpt-4",
        api_key=openai_key,
    )
    tool = typed_request(model, llmprompt, Year, city="New York")
    assert tool
    assert tool.__class__.__name__ == "Year"
    assert tool.year == 1624


@pytest.mark.asyncio
async def test_async_tool_from_json_str(llmsession: LLMSession):
    broken_json_str = '{"year": 1624, "city": "New York"'
    result = await async_tool_from_json_str(llmsession, broken_json_str, CityFoundingInfo)
    assert result.year == 1624
    assert result.city == "New York"


@pytest.mark.asyncio
async def test_async_tool_from_json_str_missing_commas(llmsession: LLMSession):
    broken_json_str = '{"year": 1624 "city": "New York"}'
    result = await async_tool_from_json_str(llmsession, broken_json_str, CityFoundingInfo)
    assert result.year == 1624
    assert result.city == "New York"


def test_tool_from_json_str(llmsession: LLMSession):
    broken_json_str = '{"year": 1624, "city": "New York"'
    result = sync_tool_from_json_str(llmsession, broken_json_str, CityFoundingInfo)
    assert result.year == 1624
    assert result.city == "New York"


def test_tool_from_json_str_missing_commas(llmsession: LLMSession):
    broken_json_str = '{"year": 1624 "city": "New York"}'
    result = sync_tool_from_json_str(llmsession, broken_json_str, CityFoundingInfo)
    assert result.year == 1624
    assert result.city == "New York"
