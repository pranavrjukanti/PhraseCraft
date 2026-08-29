import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from typing import Dict, Union
import json
import prompts as pt

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
# CONSTANTS
MODEL = "gpt-4o-mini"

# set the openai model
llm = ChatOpenAI(model=MODEL, temperature=0)


def language_corrector(text: str) -> Dict[str, Union[str, list]]:
    """
    Analyzes text for grammatical errors and returns a structured result.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary containing "original", "corrected", "language", "status",
        "errors" and "notes" — or an "error" key if the call or parse failed.
    """
    prompt = ChatPromptTemplate.from_template(pt.GRAMMAR_CHECKER_PROMPT)
    model = llm
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    try:
        response = chain.invoke({"text": text})
    except Exception as exc:
        return {"error": f"Could not reach the language model: {exc}"}

    # The model sometimes wraps its JSON in a ``` fence despite the prompt.
    cleaned = response.strip()
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        cleaned = parts[1] if len(parts) > 1 else cleaned
        if cleaned.lstrip().lower().startswith("json"):
            cleaned = cleaned.lstrip()[4:]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse response",
            "raw_response": response
        }
