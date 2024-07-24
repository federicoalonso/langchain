from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser

from third_parties.linkedin import scrape_lonkedin_profile

if __name__ == "__main__":
    load_dotenv()

    summary_template = """
    given the Linkedin information {information} about a person I wanto you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | StrOutputParser()

    linkedin_information = scrape_lonkedin_profile(linkedin_profile_url='https://linkedin.com/in/johnrmarty/', mock=True)

    res = chain.invoke(input={"information": linkedin_information})

    print(res)