from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_lonkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import Summary, summary_parser

def ice_break_with(name: str, search_context: str, scenario_context) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name, search_context)
    linkedin_data = scrape_lonkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """
        given the Linkedin information {information} about a person, and the following scenario {scenario} I want you to create:
        1. A short summary
        2. Two interesting facts about them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "scenario"], 
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data, "scenario": scenario_context})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    ice_break_with("Federico Alonso", "Uruguay desarrollador de software", "voy a entrevistarlo para un trabajo de desarrollo de software")