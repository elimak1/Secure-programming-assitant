from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.render import render_text_description

from flask import g

import os
from dotenv import load_dotenv
load_dotenv()

VECTOR_STORE_PATH = "./vector_store/owasp_faiss"
OPENAIKEY = os.getenv('OPENAI_API_KEY')
assert OPENAIKEY, 'OPENAIKEY not set'

def init_openai_agent():
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
            Use detailed and descriptive queries to get the best results.""")
        tools.append(retriever_tool)

    tool_descriptions = render_text_description(tools)

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
    Chat history:
    {chat_history}

    {input}

    {agent_scratchpad}

    {intermediate_steps}
    """

    prompt = ChatPromptTemplate.from_template(
        template=systemPrompt
    )

    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

def get_openai_agent():
    if 'openai_agent' not in g:
        g.openai_agent = init_openai_agent()
    return g.openai_agent


def invokeLLM(prompt: str, history: list = []) -> str:
    chat_history = []
    for msg in history:
        if msg["from_entity"] == "User":
            chat_history.append(HumanMessage(msg["text"]))
        else:
            chat_history.append(AIMessage(msg["text"]))

    agent_executor = get_openai_agent()
    output = agent_executor.invoke({"input": prompt, "chat_history": chat_history})
    return output["output"]