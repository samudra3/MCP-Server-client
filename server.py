from mcp.server import MCPServer

mcp= MCPServer("first mcp server testing")

@mcp.tool()
def add(a:int, b:int) -> int:
      """ it is used to add two integers"""
      return a+b

if __name__ == "__main__":
      mcp.run()