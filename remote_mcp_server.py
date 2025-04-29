# remote_mcp_server.py
import os
import json
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context
import uvicorn
import httpx

# Create a named server
mcp = FastMCP("Remote Demo Server")

# Add some useful tools


@mcp.tool()
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression.

    Args:
        expression: A mathematical expression (e.g., "2 + 3 * 4")
    """
    # Using safe eval for math expressions
    try:
        # Only allow arithmetic operations and basic math functions
        allowed_names = {"abs": abs, "max": max,
                         "min": min, "round": round, "sum": sum}
        return str(eval(expression, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def fetch_webpage(url: str, ctx: Context) -> str:
    """Fetch content from a webpage.

    Args:
        url: The URL to fetch (must start with http:// or https://)
    """
    ctx.info(f"Fetching content from {url}")

    if not url.startswith(('http://', 'https://')):
        return "Error: URL must start with http:// or https://"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            response.raise_for_status()
            return response.text[:10000]  # Limit response size
    except Exception as e:
        return f"Error fetching page: {str(e)}"


@mcp.resource("weather://{city}")
async def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: Name of the city
    """
    # This is a stub - in a real implementation, you would call a weather API
    weather_data = {
        "New York": "72°F, Partly Cloudy",
        "London": "18°C, Rainy",
        "Tokyo": "25°C, Sunny",
        "Sydney": "22°C, Clear"
    }

    if city in weather_data:
        return f"Current weather in {city}: {weather_data[city]}"
    else:
        # Simulate a more realistic response for other cities
        import random
        conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Snowy", "Clear"]
        temp = random.randint(10, 35)
        return f"Current weather in {city}: {temp}°C, {random.choice(conditions)}"


@mcp.prompt()
def analyze_text(text: str) -> str:
    """Create a prompt to analyze text content."""
    return f"""Please analyze the following text and provide insights:

{text}

In your analysis, consider:
- Main themes or topics
- Tone and sentiment
- Key insights or takeaways
- Any notable patterns or structures
"""


# Run the server when this script is executed directly
if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))

    # Create ASGI app
    app = mcp.sse_app()

    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
