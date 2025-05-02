import os
import json
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.llms import Ollama 
#from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from tools.webscrap import webscrap
from tools.linkedin_url import Linkedin_url

# Load environment variables
load_dotenv()

def generate_profile_summary_and_facts_single_step(name: str):
    # Initialize the LLM
    #llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    llm = Ollama(model="mistral", temperature=0)

    # Define tools
    tools_for_agent = [Linkedin_url, webscrap]
    
    # React agent setup
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True,handle_parsing_errors=True,max_iterations=15,
        max_execution_time=120,return_intermediate_steps=True )
    
    # Single agentic input prompt
    prompt = f"""
You are an intelligent assistant following the ReAct (Reasoning + Acting) pattern.

Your task is to:
- Search the LinkedIn URL for the given person.
- Scrape the profile information.
- Finally, summarize the profile and output the summary, interesting facts, and profile picture URL in JSON format.

Follow STRICTLY the below format:
Thought: Describe your reasoning.
Action: Name of the tool you want to use (must be EXACTLY one of: [Search LinkedIn URL, Scrap linked in page])
Action Input: Input for the tool (string)

After all actions are done, return the final output as:
Thought: I have gathered all necessary information.
Final Answer: {{"summary": "...", "interesting_facts": ["..."], "profile_pic_url": "..." }}

Only use the tools provided. If an action or observation is missing, it will cause an error.

Start!

Person Name: {input}
"""
    
    # Execute the agent
    result = agent_executor.invoke(input={"input": prompt})

        # 🔥 Print Intermediate Steps
    print("\n----- INTERMEDIATE STEPS -----")
    for step in result.get("intermediate_steps", []):
        print(f"\nAction: {step[0]}")
        print(f"Observation: {step[1]}")
    print("\n----- FINAL OUTPUT -----")

    # Create clean output dict
    output = result.get("output", {})
    raw_output = result.get("output", "")

    try:
        output = json.loads(raw_output)   # Parse string into dict
    except json.JSONDecodeError:
        print("Failed to parse output into JSON.")
        output = {}
    intermediate_steps = result.get("intermediate_steps", [])

    return {
        "summary": output.get("summary", ""),
        "interesting_facts": output.get("interesting_facts", []),
        "profile_pic_url": output.get("profile_pic_url", None),
        "intermediate_steps": intermediate_steps
    }
    return result["output"]

# Example usage
#if __name__ == "__main__":
    name = input("Enter the full name: ")
    result = generate_profile_summary_and_facts_single_step(name)
    print("Generated Output:\n", result)