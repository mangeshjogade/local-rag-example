import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
import json

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-"

# Load and prepare the document
loader = TextLoader("sample_document.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
texts = text_splitter.split_documents(documents)
print(f"Number of document chunks: {len(texts)}")

# Create embeddings and store them in a Chroma vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create a retriever from the vector store
retriever = vectorstore.as_retriever()

# Define Pydantic model for input validation
class DashboardName(BaseModel):
    dashboard_name: str = Field(..., description="The name of the dashboard to retrieve information about")

# Define the function for dashboard retrieval using @tool decorator
@tool
def get_dashboard_info(dashboard_name: str) -> str:
    """Retrieve information about a specific dashboard."""
    # Use the retriever to get relevant information
    docs = retriever.invoke(dashboard_name)  # Changed from get_relevant_documents to invoke
    # Combine the content of relevant documents
    return "\n".join([doc.page_content for doc in docs])

# Create a ChatOpenAI model with the tool bound to it
model = ChatOpenAI(model="gpt-4o").bind_tools(tools=[get_dashboard_info])  # Changed from "gpt-4o" to "gpt-4"

def process_llm_response(llm_response):
    if llm_response.additional_kwargs.get('tool_calls'):
        tool_calls = llm_response.additional_kwargs['tool_calls']
        for tool_call in tool_calls:
            function_name = tool_call['function']['name']
            function_args = tool_call['function']['arguments']
            
            if function_name == "get_dashboard_info":
                args_dict = json.loads(function_args)
                function_response = get_dashboard_info.invoke(args_dict["dashboard_name"])  # Changed from __call__ to invoke
                return function_response, tool_call['id']
    return llm_response.content, None

def ask_question(question):
    messages = [
        SystemMessage(content="You are a helpful assistant that provides information about dashboards. Use the get_dashboard_info function when you need specific information about a dashboard."),
        HumanMessage(content=question)
    ]
    
    while True:
        response = model.invoke(messages)
        result, tool_call_id = process_llm_response(response)
        
        if tool_call_id:
            messages.append(AIMessage(content=response.content, additional_kwargs={'tool_calls': response.additional_kwargs['tool_calls']}))
            messages.append(ToolMessage(content=result, tool_call_id=tool_call_id))
        else:
            print(f"Question: {question}")
            print(f"Answer: {result}")
            print("\n")
            break

# Example usage
if __name__ == "__main__":
    ask_question("Can you provide me the link to the dashboard that shows the sales performance?")
    ask_question("Can you provide dashboard for customer lifetime value?")

