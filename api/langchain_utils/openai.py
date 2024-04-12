from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain.agents import create_openai_tools_agent, AgentExecutor, create_openai_functions_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.runnables import RunnablePassthrough
from pprint import pprint
from langchain.prompts import MessagesPlaceholder



from flask import g

import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_PATH = "./vector_store/owasp_faiss"
OPENAIKEY = os.getenv('OPENAI_API_KEY')
assert OPENAIKEY, 'OPENAIKEY not set'

def init_openai_agent() -> AgentExecutor:
    llm = ChatOpenAI(openai_api_key=OPENAIKEY)

    tools = []
    # Requires vectorstore
    if os.path.exists(VECTOR_STORE_PATH):
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever()
        retriever_tool = create_retriever_tool(
            retriever,
            "owasp_doc_search",
            """Search for owasp documentation. For any questions about owasp, you must use this tool!
            Use detailed and descriptive queries to get the best results.
            Do not use the same query more than once.""")
        tools.append(retriever_tool)

    systemPrompt = """
    You are a secure coding expert named "Kev". You can engage in casual conversation but you main purpose is the following:
    Given a snippet of code or a programming concept, provide detailed advice on best practices for secure coding, referencing OWASP guidelines and other relevant security standards. Emphasize common vulnerabilities associated with the given code or concept, suggesting preventative measures and improvements. Offer examples of secure coding practices, highlighting how they adhere to recognized security protocols. Include considerations for various programming languages and frameworks where applicable, demonstrating a comprehensive understanding of security in the digital age. Ensure recommendations are current, reflecting the latest in security research and findings.

    Objective:

    Enhance code security through expert guidance and adherence to established best practices.
    Educate programmers on common vulnerabilities and how to avoid them.
    Foster a culture of security mindfulness within the programming community.

    Output Requirements:

    Clear Identification of Risks: Explicitly state potential security risks associated with the code or concept in question.
    Guideline References: Cite specific OWASP guidelines or other security standards relevant to the identified risks.
    Practical Recommendations: Offer actionable advice for mitigating risks, including code examples where possible.
    Language and Framework Specificity: Tailor advice to the specific programming language or framework involved.
    Up-to-Date Information: Ensure all recommendations reflect the latest security research and guidelines.
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", systemPrompt),
         MessagesPlaceholder("chat_history"),
         ("user", "{input}"),
         MessagesPlaceholder("agent_scratchpad")]
    )
    llm_with_tools = llm.bind(tools=[convert_to_openai_tool(tool) for tool in tools])

    agent2 = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            )
        )
        | prompt
        | condense_prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent2, tools=tools, verbose=True, max_iterations=10)
    return agent_executor, llm

def condense_prompt(prompt: ChatPromptValue) -> ChatPromptValue:
    messages = prompt.to_messages()
    llm = get_openai_llm()
    num_tokens = llm.get_num_tokens_from_messages(messages)
    ai_function_messages = messages[1:]
    while num_tokens > 8_000:
        ai_function_messages = ai_function_messages[1:]
        num_tokens = llm.get_num_tokens_from_messages(
            messages[:1] + ai_function_messages
        )
    messages = messages[:1] + ai_function_messages
    return ChatPromptValue(messages=messages)

def get_openai_agent() -> AgentExecutor:
    if 'openai_agent' not in g:
        agent, llm = init_openai_agent()
        g.openai_agent = agent
        g.llm = llm
    return g.openai_agent

def get_openai_llm() -> ChatOpenAI:
    if 'llm' not in g:
        agent, llm = init_openai_agent()
        g.openai_agent = agent
        g.llm = llm
    return g.llm



def invokeLLM(prompt: str, history: list = []) -> str:
    chat_history = []
    for msg in history:
        if msg["from_entity"] == "User":
            chat_history.append(HumanMessage(msg["text"]))
        else:
            chat_history.append(AIMessage(msg["text"]))

    agent_executor = get_openai_agent()
    agent_response = agent_executor.invoke({"input": prompt, "chat_history": chat_history})
    return agent_response["output"]