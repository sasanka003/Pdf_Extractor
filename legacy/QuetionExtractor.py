# import json
# from langchain.agents import initialize_agent, Tool
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# current_dir = os.path.dirname(os.path.abspath(__file__))
# json_file = os.path.join(current_dir, "output", "combined.json")
# output_file = os.path.join(current_dir, "output", "output.json")

# # Function to read the JSON file
# def read_json_file(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# # Function to write the extracted data to a new JSON file
# def write_json_file(data, output_file):
#     with open(output_file, 'w') as file:
#         json.dump(data, file, indent=2)

# # Function to analyze the JSON content and extract required information
# def analyze_json(content):
#     llm = OpenAI(temperature=0)
    
#     prompt = PromptTemplate(
#         input_variables=["json_content"],
#         template="""
#         Analyze the following JSON content and extract:
#         1. Question
#         2. Allocated points
#         3. Answers
#         4. Correct answer
#         5. Justification for the correct answer

#         JSON content:
#         {json_content}

#         Provide the extracted information in a JSON format.
#         """
#     )
    
#     chain = LLMChain(llm=llm, prompt=prompt)
#     result = chain.run(json_content=json.dumps(content))
    
#     return json.loads(result)

# # Create tools for the agent
# tools = [
#     Tool(
#         name="ReadJSON",
#         func=read_json_file,
#         description="Reads a JSON file and returns its content"
#     ),
#     Tool(
#         name="AnalyzeJSON",
#         func=analyze_json,
#         description="Analyzes JSON content and extracts required information"
#     ),
#     Tool(
#         name="WriteJSON",
#         func=write_json_file,
#         description="Writes data to a JSON file"
#     )
# ]

# # Initialize the agent
# llm = OpenAI(model="gpt-4o-mini", temperature=0)
# agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# # Run the agent
# result = agent.run({
#     "input_file": json_file,
#     "output_file": output_file
# })

# print(result)


from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an expert analyzer. Analyze the text of each of the json object and extract:
          1. Question
          2. Allocated points
          3. Answers
          4. Correct answer
          5. Justification for the correct answer
 
         and return in below json format:
            {
            "question": Question,
            "allocated_points": Allocated points,
            "answers": [
                Answers
            ],
            "correct_answer": Correct answer,
            "justification": Justification for the correct answer
            }"""),
        ("human", "use these json objects and analyze {product_name}."),
    ]
)


# Define pros analysis step
def analyze_pros(features):
    pros_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert product reviewer."),
            (
                "human",
                "Given these features: {features}, list the pros of these features.",
            ),
        ]
    )
    return pros_template.format_prompt(features=features)


# Define cons analysis step
def analyze_cons(features):
    cons_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert product reviewer."),
            (
                "human",
                "Given these features: {features}, list the cons of these features.",
            ),
        ]
    )
    return cons_template.format_prompt(features=features)


# Combine pros and cons into a final review
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"


# Simplify branches with LCEL
pros_branch_chain = (
    RunnableLambda(lambda x: analyze_pros(x)) | model | StrOutputParser()
)

cons_branch_chain = (
    RunnableLambda(lambda x: analyze_cons(x)) | model | StrOutputParser()
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)

# Run the chain
result = chain.invoke({"product_name": "MacBook Pro"})

# Output
print(result)