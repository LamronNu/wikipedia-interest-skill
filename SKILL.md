---
name: wikipedia-interest
description: Analyze Wikipedia pageview data to study interest in topics over time.
---

# Wikipedia Interest Analysis

## Purpose

Use this skill to retrieve Wikipedia pageview data and analyze interest in a topic over time.

## Workflow

1. Identify the Wikipedia language edition.
2. Identify the article title.
3. Identify the requested date range.
4. Use the `get_pageviews` tool to retrieve pageview data.
5. Use the `analyze_trend` tool to calculate basic trend metrics.
6. Base conclusions about trends only on retrieved data and tool results.
7. Do not invent pageview values or calculated metrics.
8. Mention important limitations when interpreting pageviews.
9. Use `create_chart` when a visualization is requested or useful for communicating the results.

## Data source

Wikimedia Pageviews API:
https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html

## Important limitations

- Wikipedia pageviews are a proxy for attention, not willingness to pay.
- A pageview increase does not by itself prove growing long-term interest.
- Short-term spikes should not automatically be interpreted as a trend.

## Available tools

### get_pageviews

Retrieves daily Wikipedia pageview data for a specified article, language edition and date range.

### analyze_trend

Analyzes retrieved pageview data and returns basic metrics including:

- start and end pageviews;
- percentage change;
- total pageviews;
- average and median daily pageviews;
- simple overall trend;
- maximum and minimum daily pageviews and their dates.

Use `analyze_trend` only on data returned by `get_pageviews`.

### create_chart

Creates a line chart from Wikipedia pageview data and saves it as a PNG image.

Use `create_chart` when the user asks for a visualization or when a chart would help communicate the results.

The tool requires:
- pageview data returned by `get_pageviews`;
- an output file path.

The chart should show:
- date on the X-axis;
- daily pageviews on the Y-axis.

Do not invent or modify pageview values before creating the chart.