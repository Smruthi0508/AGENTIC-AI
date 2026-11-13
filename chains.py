"""LCEL chains: prompt | llm | parser."""
import json
from functools import lru_cache

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from categories import SPEND_CATEGORIES
from llm import get_llm
from prompts import (
    CATEGORIZER_EXAMPLES, CATEGORIZER_HUMAN, CATEGORIZER_SYSTEM, CATEGORY_LIST,
    EXPLAINER_HUMAN, EXPLAINER_SYSTEM, ROUTER_EXAMPLES, ROUTER_HUMAN, ROUTER_SYSTEM,
)


@lru_cache(maxsize=1)
def get_chains():
    llm = get_llm()

    def make(system, human):
        return ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    router = make(ROUTER_SYSTEM, ROUTER_HUMAN) | llm | JsonOutputParser()
    explainer = make(EXPLAINER_SYSTEM, EXPLAINER_HUMAN) | llm | StrOutputParser()
    categorizer = make(CATEGORIZER_SYSTEM, CATEGORIZER_HUMAN) | llm | JsonOutputParser()
    return router, explainer, categorizer


def run_router(message, months):
    router, _, _ = get_chains()
    return router.invoke({
        "categories": CATEGORY_LIST, "months": ", ".join(months),
        "examples": ROUTER_EXAMPLES, "message": message,
    })


def run_explainer(**kwargs):
    _, explainer, _ = get_chains()
    return explainer.invoke(kwargs)


def llm_categorize(merchants):
    """merchant names -> {merchant: category}"""
    _, _, categorizer = get_chains()
    out = categorizer.invoke({
        "categories": CATEGORY_LIST, "examples": CATEGORIZER_EXAMPLES,
        "items": json.dumps({str(i): m for i, m in enumerate(merchants)}, ensure_ascii=False),
    })
    result = {}
    for i, m in enumerate(merchants):
        cat = out.get(str(i)) if isinstance(out, dict) else None
        result[m] = cat if cat in SPEND_CATEGORIES else "Other"
    return result
