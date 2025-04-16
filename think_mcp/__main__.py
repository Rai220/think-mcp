from mcp.server.fastmcp import FastMCP
from pydantic import Field
from dotenv import load_dotenv, find_dotenv
import argparse
import json

load_dotenv(find_dotenv())

mcp = FastMCP("think_mcp")
tavily_client = None

advanced_mode = False  # default, may be set in main()

@mcp.prompt()
def system() -> str:
    return """## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness 

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Economy class × 3 passengers
  * If regular member: 1 free bag each → 3 extra bags = $150
  * If silver member: 2 free bags each → 0 extra bags = $0
  * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>"""

@mcp.tool()
async def think(thought: str = Field(..., description="A thought to think about.")) -> str:
    """Use the tool to think about something. 
It will not obtain new information or change the database, but just append the thought to the log. 
Use it when complex reasoning or some cache memory is needed."""
    return thought

parser = argparse.ArgumentParser(description="Think MCP server")
parser.add_argument('--advanced', action='store_true', help='Enable advanced mode (plan, search, criticize tools)')
args = parser.parse_args()

if args.advanced:
    print("Advanced mode enabled. Loading advanced tools...")
    
    @mcp.tool()
    async def criticize(criticism: str = Field(..., description="Сonstructive criticism")) -> str:
        """Use the tool to critic your steps. 
        It will not obtain new information or change the database, but just append the thought to the log. 
        Use it when complex reasoning or some cache memory is needed."""
        return criticism

    @mcp.tool()
    async def plan(plan: str = Field(..., description="A plan of next steps")) -> str:
        """Use the tool to plan your steps. 
        It will not obtain new information or change the database, but just append the thought to the log. 
        Use it when complex reasoning or some cache memory is needed."""
        return plan

    @mcp.tool()
    async def search(query: str = Field(..., description="Search query")) -> str:
        """Search the web for a given query."""
        from tavily import TavilyClient
        tavily_client = TavilyClient()
        context = tavily_client.get_search_context(query=query)
        return json.dumps(context, ensure_ascii=False)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
