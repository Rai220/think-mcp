from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("think_mcp")

@mcp.tool()
async def think(thought: str = Field(..., description="A thought to think about.")) -> str:
    """Use the tool to think about something. It will not obtain new information or change the database, 
but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.
    """
    return thought

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
