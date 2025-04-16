# Think MCP Tool

Think MCP is an implementation of an MCP (Model Context Protocol) server that provides a "think" tool for structured reasoning in agentic AI workflows. This project is inspired by the Anthropic engineering article: [The "think" tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool).

According to the referenced article, adding the think tool can lead to improved evaluation metrics by enabling reasoning capabilities even in models that do not natively possess advanced reasoning skills.

![alt text](tau_bench.png)

## What is the "think" tool?
The "think" tool allows an AI agent to pause and record an explicit thought during complex reasoning or multi-step tool use. It does not change the environment or database, but appends the thought to the log, helping the agent process information, backtrack, or comply with detailed policies.

This approach is especially useful for:
- Tool output analysis (processing results of previous tool calls)
- Policy-heavy environments (verifying compliance with guidelines)
- Sequential decision making (where each step builds on previous ones)

## Features
- Implements the "think" tool as described in Anthropic's research
- Minimal, standards-based MCP server using [mcp[cli]](https://pypi.org/project/mcp/)
- Ready for integration with Claude or other agentic LLMs

## Usage

### MCP server configuration
Add this MCP server to your facorite agent.
```
"mcpServers": {
    "think-mcp": {
        "command": "uvx",
        "args": ["think-mcp"],
        "enabled": true
    }
}
```

## Tool definition
The "think" tool is defined as:
- **Input:** `thought` (string) — A thought to think about.
- **Behavior:** Appends the thought to the log for structured reasoning.

## Advanced mode
Adds aditional tools for your agent:
- criticize
- plan
- search

```
"mcpServers": {
    "think-mcp": {
        "command": "uvx",
        "args": ["think-mcp", "--advanced"],
        "enabled": true,
        "env": {
            "TAVILY_API_KEY": ... YOUR TAVILY API KEY HERE ...
        }
    }
}
```

## Reference
- Based on: [Anthropic Engineering Blog — The "think" tool](https://www.anthropic.com/engineering/claude-think-tool)

## License
MIT License — see [LICENSE](LICENSE)