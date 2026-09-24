import os
from pathlib import Path

from openai import OpenAI

from scripts.wikipedia import get_pageviews


# --------------------------------------------------
# 1. Load the Skill instructions
# --------------------------------------------------

skill_path = Path("SKILL.md")
skill = skill_path.read_text(encoding="utf-8")


# --------------------------------------------------
# 2. Connect to OpenRouter
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


# --------------------------------------------------
# 3. Define the Wikipedia tool
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pageviews",
            "description": (
                "Get daily Wikipedia pageviews for an article "
                "in a specific language and date range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Wikipedia language code, e.g. uk or pl."
                    },
                    "article": {
                        "type": "string",
                        "description": "Wikipedia article title."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYYMMDD format."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYYMMDD format."
                    },
                },
                "required": [
                    "language",
                    "article",
                    "start_date",
                    "end_date",
                ],
            },
        },
    }
]


# --------------------------------------------------
# 4. Ask the model to handle the user's request
# --------------------------------------------------

user_request = input("Your request: ")

messages = [
    {
        "role": "system",
        "content": skill,
    },
    {
        "role": "user",
        "content": user_request,
    },
]


response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=tools,
)


message = response.choices[0].message


# --------------------------------------------------
# 5. Execute the tool if the model requested it
# --------------------------------------------------

if message.tool_calls:

    messages.append(message)

    for tool_call in message.tool_calls:

        if tool_call.function.name == "get_pageviews":

            import json

            arguments = json.loads(tool_call.function.arguments)

            result = get_pageviews(
                language=arguments["language"],
                article=arguments["article"],
                start_date=arguments["start_date"],
                end_date=arguments["end_date"],
            )

            # Convert DataFrame to JSON-like text
            result_text = result.to_json(
                orient="records",
                date_format="iso"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_text,
                }
            )


    # --------------------------------------------------
    # 6. Ask the model to explain the result
    # --------------------------------------------------

    final_response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    print("\nAgent:\n")
    print(final_response.choices[0].message.content)

else:

    print("\nAgent:\n")
    print(message.content)
