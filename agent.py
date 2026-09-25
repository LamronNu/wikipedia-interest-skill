import os
import json
import pandas as pd
from pathlib import Path

from openai import OpenAI

from scripts.wikipedia import get_pageviews
from scripts.analyze import analyze_trend
from scripts.charts import create_chart


# --------------------------------------------------
# 1. Load the Skill instructions
# --------------------------------------------------

skill_path = Path("SKILL.md")
skill = skill_path.read_text(encoding="utf-8")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


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
# datastore
data_store = {}

# make data name------------
import re


def make_data_id(language, article, start_date, end_date):
    safe_article = article.lower()

    # Replace Cyrillic characters with a simple generic topic name
    # for filenames/data IDs.
    transliteration = {
        "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g",
        "д": "d", "е": "e", "є": "ie", "ж": "zh", "з": "z",
        "и": "y", "і": "i", "ї": "i", "й": "i", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
        "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
        "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
        "щ": "shch", "ь": "", "ю": "iu", "я": "ia",
        "ё": "io", "ъ": "", "ы": "y", "э": "e",
    }

    safe_article = "".join(
        transliteration.get(char, char)
        for char in safe_article
    )

    safe_article = re.sub(r"[^a-z0-9]+", "_", safe_article)
    safe_article = safe_article.strip("_")

    return f"{language}_{safe_article}_{start_date}_{end_date}"
# -------------------------------

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
    },
    {
      "type": "function",
      "function": {
          "name": "analyze_trend",
          "description": "Analyze pageview data previously retrieved by get_pageviews.",
          "parameters": {
              "type": "object",
              "properties": {
                  "data_id": {
                      "type": "string"
                  }
              },
              "required": [
                  "data_id"
              ]
          }
      }
  },
  {
      "type": "function",
      "function": {
          "name": "create_chart",
          "description": "Create a chart from pageview data previously retrieved by get_pageviews.",
          "parameters": {
              "type": "object",
              "properties": {
                  "data_id": {
                      "type": "string",
                      "description": "ID of the pageview dataset stored by get_pageviews."
                  }
              },
              "required": ["data_id"]
          }
      }
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
    model="openrouter/free", # model="qwen/qwen3.8-27b:free",
    messages=messages,
    tools=tools,
)
# debug--
# print("TOOL CALLS:")
# print(response.choices[0].message.tool_calls)

# print("CONTENT:")
# print(response.choices[0].message.content)
# end debug--

message = response.choices[0].message


# --------------------------------------------------
# 5. Execute the tool if the model requested it
# --------------------------------------------------

if message.tool_calls:

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # -----------------------------------------
        # GET PAGEVIEWS
        # -----------------------------------------

        if tool_name == "get_pageviews":

            language = arguments["language"]
            article = arguments["article"]
            start_date = arguments["start_date"]
            end_date = arguments["end_date"]

            result = get_pageviews(
                language,
                article,
                start_date,
                end_date
            )

            data_id = make_data_id(
                language,
                article,
                start_date,
                end_date
            )

            data_store[data_id] = result
            # create chart
            os.makedirs("outputs", exist_ok=True)

            chart_path = os.path.join(
                "outputs",
                f"{data_id}.png"
            )

            create_chart(
                result,
                chart_path
            )
            # --

            result_text = json.dumps(
                {
                    "status": "ok",
                    "data_id": data_id,
                    "rows": len(result),
                    "start_date": result["date"].min().strftime("%Y-%m-%d"),
                    "end_date": result["date"].max().strftime("%Y-%m-%d"),
                    "chart_path": chart_path,
                },
                ensure_ascii=False
            )

        # -----------------------------------------
        # ANALYZE TREND
        # -----------------------------------------

        elif tool_name == "analyze_trend":

            data_id = arguments["data_id"]

            if data_id not in data_store:
                result_text = json.dumps(
                    {
                        "status": "error",
                        "message": f"Unknown data_id: {data_id}"
                    },
                    ensure_ascii=False
                )

            else:
                data = data_store[data_id]

                result = analyze_trend(data)

                result_text = json.dumps(
                    result,
                    ensure_ascii=False
                )

        # -----------------------------------------
        # CREATE CHART
        # -----------------------------------------

        elif tool_name == "create_chart":

          data_id = arguments["data_id"]

          if data_id not in data_store:
              result_text = json.dumps(
                  {
                      "status": "error",
                      "message": f"Unknown data_id: {data_id}"
                  },
                  ensure_ascii=False
              )

          else:
              data = data_store[data_id]

              os.makedirs("outputs", exist_ok=True)

              output_path = os.path.join(
                  "outputs",
                  f"{data_id}.png"
              )

              result = create_chart(
                  data,
                  output_path
              )

              result_text = json.dumps(
                  {
                      "status": "ok",
                      "data_id": data_id,
                      "chart_path": result
                  },
                  ensure_ascii=False
              )
        # -----------------------------------------
        # UNKNOWN TOOL
        # -----------------------------------------

        else:

            result_text = json.dumps(
                {
                    "status": "error",
                    "message": f"Unknown tool: {tool_name}"
                },
                ensure_ascii=False
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
        model="openrouter/free", # model="qwen/qwen3.8-27b:free", 
        messages=messages,
    )
    # debug--
    # print("\nFINAL RESPONSE OBJECT:")
    # print(final_response.choices[0].message)
    # end debug--
    print("\nAgent:\n")
    print(final_response.choices[0].message.content)

else:

    print("\nAgent:\n")
    print(message.content)
