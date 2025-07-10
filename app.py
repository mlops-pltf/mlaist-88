import asyncio
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


from dotenv import load_dotenv
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


client = MultiServerMCPClient(
    {
        "weather": {
            # Ensure you start your weather server on port 8000
            "url": "https://mlops-pltf-mcp-sentiment.hf.space/gradio_api/mcp/sse",
            "transport": "sse",
        }
    }
)

async def get_response(message:str):
    chat_llm = ChatOpenAI(model="gpt-4o")
    tools = await client.get_tools()
    agent = create_react_agent(
        chat_llm,
        tools
    )
    return await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": f"Analyze the sentiment of the following text '{message}'"}
        ]}
    )

def get_final_response(message:str) -> str:
    result = asyncio.run(get_response(message))
    return result['messages'][-1].content

# print(get_final_response('The football matche was incredibly boring!!'))
demo = gr.ChatInterface(
    fn=lambda message, history: get_final_response(message),
    type="messages",
    examples=["Provide the message to analyze"],
    title="Agent with MCP Tools",
    description="This is a simple agent that uses MCP tools to answer questions.",
)

demo.launch()