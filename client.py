import asyncio
import sys
import os
from google import genai
from google.genai import types
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
      client= genai.Client(
            api_key= os.environ["GEMINI_API_KEY"]
      )
      server_params= StdioServerParameters(
            command=sys.executable,
            args=["server.py"]
      )
      async with stdio_client(server_params) as (read,write):
            async with ClientSession(read,write) as session:
                  await session.initialize()
                  tools= await session.list_tools()
                  declarations=[
                        types.FunctionDeclaration(
                              name=tool.name,
                              description=tool.description or "",
                              parameters_json_schema=tool.input_schema
                        )
                        for tool in tools.tools

                  ]
                  gemini_tools= [
                        types.Tool(
                              function_declarations=declarations
                        )
                  ]
                  # for tool in gemini_tools[0].function_declarations:
                  #       print("name: ",tool.name)
                  #       print("schema: ",tool.parameters_json_schema)
                  response= await client.aio.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents="What is 10 plus 30? Use the add_numbers tool.",
                        config= types.GenerateContentConfig(
                              tools=gemini_tools,
                              temperature=0
                        )
                  )
                  function_call=response.function_calls[0]
                  result= await session.call_tool(
                        function_call.name,
                        arguments=function_call.args
                  )

                  print(result.content)
                  await client.aio.aclose()

                  # tools= await session.list_tools()
                  # for tool in tools.tools:
                  #       print(tool.name)
                  #       print(tool.description)
                  #       print(tool.input_schema)
                  # result = await session.call_tool(
                  #       name="add",
                  #       arguments={"a":10,"b":30}
                  # )
                  # print("tool_result: ",result.content)

if __name__ == "__main__":
      asyncio.run(main())
