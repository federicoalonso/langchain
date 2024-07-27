from typing import Union
from dotenv import load_dotenv
from langchain.agents import tool, Tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.prompts.prompt import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.schema import AgentAction, AgentFinish

load_dotenv()

@tool
def get_text_Length(text:str) -> int:
    """Returns the length of the text by character count"""
    text = text.strip("'\n").strip('"')
    print("***************************************************")
    return len(text)

def find_tool_by_name(name:str, tools: list[Tool]) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool {name} not found in available tools")

if __name__ == '__main__':
    tools = [get_text_Length]

    template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}] and only the name of the tool
        Action Input: the input to the action as you would type it in the tool
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: If you already have an observation and it is accurate, I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), 
        tool_names= ", ".join([tool.name for tool in tools])
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", stop_sequences=["\nObservation:"])
    model = OllamaLLM(model="llama3.1", temperature=0, stop=["\nObservation:"])

    intermediate_steps = []
    
    agent = {
        "input": lambda x:x["input"],
        "agent_scratchpad": lambda x:format_log_to_str(x["agent_scratchpad"]),
        } | prompt | model | ReActSingleInputOutputParser()

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": "What is the length of 'Hello, world' in characters?",
            "agent_scratchpad": intermediate_steps
        }
    )

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tool_name, tools)
        if tool_to_use:
            tool_input = agent_step.tool_input
            observation = tool_to_use.func(str(tool_input))
            print(observation)
            intermediate_steps.append((agent_step, str(observation)))
            print(intermediate_steps)
            agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                {
                    "input": "What is the length of 'Hello, world' in characters?",
                    "agent_scratchpad": intermediate_steps
                }
            )
            print(agent_step)
            if isinstance(agent_step, AgentFinish):
                print(agent_step.return_values)
        else:
            raise ValueError(f"Tool {tool_name} not found in available tools")