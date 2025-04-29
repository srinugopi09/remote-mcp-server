from fastmcp import FastMCP

mcp = FastMCP(
    name="echo-server",
    version="0.0.1",
)


@mcp.tool(description="Return whatever text you pass in.")
def echo(text: str) -> str:           # ← tool signature
    return text                       # ← tool implementation


if __name__ == "__main__":
    # Expose an SSE endpoint at http://<host>:8080/sse
    mcp.run(host="0.0.0.0", port=8080, transport="sse")
