import json
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnableLambda
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_dir, "output", "combined.json")
output_file = os.path.join(current_dir, "output", "output.json")

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4")

# Define the output structure
class ExtractedData(BaseModel):
    filename: str = Field(description="The filename of the processed document")
    question: str = Field(description="The extracted question")
    allocated_points: int = Field(description="The number of points allocated to the question")
    options: list[str] = Field(description="All the options given to select the answer")
    correct_answer: int = Field(description="The correct answer")
    justification: str = Field(description="The justification for the correct answer and why other options are incorrect")

# Create a parser
parser = PydanticOutputParser(pydantic_object=ExtractedData)

# Define prompt templates
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert extractor. Extract the question, allocated points, answer, correct answer and justification from the given text. Format your response as JSON."),
    ("human", "Use the following text to extract the required information:\n\n{text}\n\n{format_instructions}")
])



# Create the LLMChain
chain = (
    prompt_template | model | parser
)

# Function to append JSON to file
def append_json_to_file(json_object, filename=output_file):
    try:
        with open(filename, 'r+') as file:
            # Load existing data
            file_data = json.load(file)
            # Append new data
            file_data.append(json_object)
            # Set file's current position at offset
            file.seek(0)
            # Convert back to JSON and write
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        # If file doesn't exist, create it and add the first item
        with open(filename, 'w') as file:
            json.dump([json_object], file, indent=4)

# Function to process a single JSON object
def process_json_object(json_obj):
    filename = json_obj['filename']
    text = json_obj['text']
    
    # Run the chain
    result = chain.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    
    # Add filename to the result
    result_dict = result.dict()
    result_dict['filename'] = filename
    
    # Append to file
    append_json_to_file(result_dict)
    
    return result_dict

# Function to read JSON file and process each object
def process_json_file(input_filename, output_filename='output.json'):
    with open(input_filename, 'r') as file:
        json_data = json.load(file)
    
    results = []
    for json_obj in json_data:
        result = process_json_object(json_obj)
        results.append(result)
    
    return results

# Example usage
input_filename = json_file  # Replace with your input JSON file name
results = process_json_file(input_filename)

# Print results (optional)
for result in results:
    print(json.dumps(result, indent=2))
    print("---")