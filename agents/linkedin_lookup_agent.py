import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup(name: str, context: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    template = """given the full name {name_of_person} and this context to refine the search {context_of_search} I want you to get it me a link to their Linkedin profile page. Your answer should contain only a URL."""
    prompt_template = PromptTemplate(input_variables=["name_of_person", "context_of_search"], template=template)
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func = get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name, context_of_search=context)}
        )
    
    linkedin_profile_url = result["output"]
    return linkedin_profile_url