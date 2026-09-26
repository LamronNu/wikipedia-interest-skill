# Wikipedia Interest Skill

An experimental Agent Skill for analyzing Wikipedia pageview data and exploring changes in interest in a topic over time.

## 1. About the project

This project was created as a take-home assignment for an AI Agent Skill that helps B2C product teams explore audience interest using Wikipedia pageview statistics.

The original task is available here:

**[Task description](https://gist.github.com/edugenesis/84f332ba58642cf12110b196775a8b72)**

The skill uses the [Wikimedia Pageviews API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html) to retrieve pageview data for Wikipedia articles, analyze trends, and generate charts.

## 2. Project scope

I had very limited previous experience with building AI Agent Skills, tool calling, and agent-based workflows.

Therefore, the goal of this implementation was intentionally practical and limited:

* build the simplest working version;
* understand how an Agent Skill interacts with an agent;
* implement and test the core data flow;
* test it with an LLM;
* document the current limitations and possible next steps.

The project is therefore a **minimal working prototype rather than a production-ready skill**.

## 3. What is implemented

The current version contains three main functions.

### `get_pageviews()`

Retrieves daily pageview statistics for a Wikipedia article for a specified language and date range using the Wikimedia Pageviews API.

Example:

```text
Get the pageviews for the Ukrainian Wikipedia article "Astronomy"
during January 2026.
```

### `analyze_trend()`

Analyzes the retrieved pageview data and provides a basic trend summary.

It is used to identify whether interest increased or decreased over the selected period and provides quantitative information supporting the conclusion.

Example:

```text
Analyze the trend of the pageviews for the Ukrainian Wikipedia article
"Astronomy" during January 2026.
```

### `create_chart()`

Creates a line chart from the retrieved pageview data and saves it as a PNG file.

Example:

```text
Show the pageviews for the Ukrainian Wikipedia article "Astronomy"
during January 2026 and create a chart.
```

The generated chart is stored in the `outputs/` directory.

## 4. Example agent requests

The skill was tested with requests such as:

```text
Get the pageviews for the Ukrainian Wikipedia article "Астрономія"
during January 2026 and create a chart.
```

and:

```text
Show the pageviews for the Ukrainian Wikipedia article "Астрономія"
during January 2026 and analyze the trend in Ukrainian.
```

The agent was also tested with a more natural-language request:

```text
Покажи перегляди статті «Україна» в україномовній Wikipedia
за серпень 2026 року і створи графік. Проаналізуй українською мовою.
```

## 5. Testing and lessons learned

The implementation was developed and tested in Google Colab and then transferred to GitHub.

Several practical issues appeared during development:

1. **The skill instructions matter.**
   At one point a function worked correctly when called directly, but the agent did not use it because the corresponding instructions were not properly described in `SKILL.md`. This demonstrated that implementing a function alone is not enough: the agent also needs clear instructions about when and how to use it.

2. **Different models handle tools differently.**
   During testing, different OpenRouter models did not always behave in the same way. Some models correctly produced structured tool calls, while another model sometimes generated text that looked like a tool call instead of actually invoking the function.

3. **Free model availability and stability can vary.**
   Some requests were affected by provider rate limits or slow responses. In one case the agent appeared to hang for several minutes before a repeated request completed successfully.

4. **Deterministic code is useful around an LLM.**
   The actual data retrieval, analysis, and chart generation are performed by Python functions. The agent is used to interpret the user's request and connect the appropriate operations rather than relying on the model to perform the data processing itself.

These limitations are important considerations for a more robust version of the skill.

## 6. Possible future development

If more development time were available, the skill could be extended in several stages.

### 1. Compare languages and audiences

Add a function for comparing the same topic across multiple Wikipedia language editions. The agent could calculate relative growth, absolute changes, and other comparable metrics and identify differences between selected audiences.

### 2. Improve statistical analysis

Add more robust trend analysis, including moving averages, year-over-year comparisons, seasonality, outlier detection, and confidence or reliability indicators. The skill should distinguish between a genuine long-term trend and short-term spikes caused by external events.

### 3. Support related and repeated analyses

Introduce structured intermediate datasets that can be reused across multiple operations. This would allow the agent to retrieve data once and then perform several analyses, comparisons, or visualizations without requesting the same data again.

### 4. Generate shareable reports

Add PDF report generation with a one-page summary containing the key findings, charts, methodology, assumptions, and limitations. The report should be generated from the same structured data used by the analysis functions.

### 5. Improve validation and reliability

Add validation of Wikipedia article names, language codes, date ranges, missing data, API errors, and unusual pageview patterns. The agent should also verify that its conclusions are supported by the retrieved data before presenting recommendations.

### 6. Test with stronger and more reliable agent models

The skill should be tested with the model specified in the original assignment, such as Claude Haiku 4.5, as well as other models with reliable structured tool-calling support. This would make it possible to separate limitations of the skill itself from limitations of a particular free model or provider.

## 7. Conclusion

This project resulted in a minimal working Wikipedia analysis skill that can retrieve pageview data, analyze a basic trend, and generate a visualization through an AI agent.

The main goal was not to build a complete production system, but to learn how an Agent Skill is structured, how Python functions can be exposed to an agent as tools, how data can be passed between operations, and how an agent interacts with those tools.

The project also provided practical experience with model-specific tool-calling behavior, debugging agent workflows, testing in Google Colab, and packaging the result as a GitHub repository.

## 8. Resources and Tools

The following tools were used during the development of the project:

* **ChatGPT** — for analyzing the assignment, exploring the Agent Skills concept and related technologies, designing the implementation approach, and developing the main part of the code.
* **Google Colab** — for writing, running, and testing Python code in an accessible development environment.
* **Google Gemini** — for troubleshooting minor coding issues, clarifying technical questions, and validating individual implementation details.

This project was also a learning exercise: prior to this assignment, I had not worked with Google Colab, Python-based Agent Skills, or agent tool-calling workflows.

