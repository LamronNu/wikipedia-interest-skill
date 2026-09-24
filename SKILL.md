---
name: wikipedia-interest
description: Analyze Wikipedia pageview data to study interest in topics over time.
---

# Wikipedia Interest Analysis

## Purpose

Use this skill to retrieve Wikipedia pageview data and analyze interest in a topic over time.

## Workflow

1. Identify the Wikipedia language, article and date range from the user request.
2. Use the `get_pageviews` function to retrieve pageview data.
3. Check whether data was returned successfully.
4. Summarize the observed pageviews.
5. Generate a simple time-series chart when requested.

## Data source

Wikimedia Pageviews API:
https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html

## Important limitations

- Wikipedia pageviews are a proxy for attention, not willingness to pay.
- A pageview increase does not by itself prove growing long-term interest.
- Short-term spikes should not automatically be interpreted as a trend.
