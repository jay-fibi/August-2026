# Jay - Simple Greeting MCP Server
"""A minimal Model Context Protocol (MCP) server exposing greeting tools.

Runs over stdio, which is the transport Cline uses for local MCP servers.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jay-greeting-server")

GREETING_STYLES = {
    "casual": "Hey {name}!",
    "formal": "Good day, {name}. It is a pleasure to meet you.",
    "friendly": "Hello, {name}! Hope you're having a great day.",
    "enthusiastic": "HELLO {name}!!! So awesome to see you!",
}


@mcp.tool()
def jay_greet(name: str, style: str = "friendly") -> str:
    """Greet a person by name.

    Args:
        name: The name of the person to greet.
        style: One of casual, formal, friendly, enthusiastic.
    """
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Name must not be empty.")

    key = style.strip().lower()
    if key not in GREETING_STYLES:
        raise ValueError(
            f"Unknown style '{style}'. Choose one of: {', '.join(sorted(GREETING_STYLES))}"
        )

    return GREETING_STYLES[key].format(name=clean_name)


@mcp.tool()
def jay_greet_many(names: list[str], style: str = "friendly") -> list[str]:
    """Greet several people at once.

    Args:
        names: The names of the people to greet.
        style: One of casual, formal, friendly, enthusiastic.
    """
    if not names:
        raise ValueError("Provide at least one name.")
    return [jay_greet(name, style) for name in names]


@mcp.tool()
def jay_list_greeting_styles() -> list[str]:
    """List the greeting styles supported by this server."""
    return sorted(GREETING_STYLES)


if __name__ == "__main__":
    mcp.run(transport="stdio")
