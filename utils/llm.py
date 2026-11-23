from langchain_ollama import ChatOllama

# Initialize local LLM
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.0,
    num_predict=900,
    num_ctx=4096
)

def get_llm_response(prompt):
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    result = get_llm_response(
        "Explain what a research paper is in simple language."
    )
    print(result)
