# call-center-analysis
# Call Center Data Analysis

## Project Overview

This project analyzes call center performance using operational and customer experience data.

The analysis focuses on:

- Data cleaning and validation
- Call center KPI calculation
- Team-level performance analysis
- Root cause investigation
- Management findings and recommendations
- A FastAPI backend for accessing calculated KPIs with filters

## Dataset

The dataset contains call-level records with information about:

- Call date and start time
- Customer and agent information
- Team/queue
- Call reason and channel
- Call status
- Wait, handle, hold, and after-call work times
- Customer satisfaction (CSAT)
- First Contact Resolution (FCR)
- Transfer count

The original dataset contained 968 records and 16 columns.

After data cleaning and validation, the final dataset contains 964 records and 20 columns.

## Data Cleaning

The following data quality checks and cleaning steps were performed:

- Checked missing values and duplicate records.
- Identified and handled negative handle time values.
- Investigated duplicate Call IDs and removed an inconsistent duplicate record.
- Investigated missing agent IDs and retained them when no reliable value could be inferred.
- Checked logical consistency between call status and handle time.
- Excluded handle time from abandoned calls when it was not meaningful for KPI calculation.
- Validated date and time formats.
- Investigated potentially unusual CSAT values and retained them because the dataset documentation did not define a strict CSAT scale.
- Created derived variables such as cleaned handle time, hour, and shift.

## KPI Analysis

The following call center KPIs were calculated:

| KPI            | Definition                                                                        |
| -------------- | --------------------------------------------------------------------------------- |
| Answer Rate    | Percentage of calls handled by an agent, including Answered and Transferred calls |
| Abandon Rate   | Percentage of calls abandoned before being handled                                |
| AWT            | Average Wait Time before the call is handled or abandoned                         |
| AHT            | Average Handle Time for valid handled calls                                       |
| CSAT           | Average Customer Satisfaction score                                               |
| FCR            | Percentage of valid contacts resolved during the first contact                    |
| Transfer Rate  | Percentage of calls transferred to another agent/team                             |
| ACW            | Average After Call Work time                                                      |
| Contact Volume | Total number of calls                                                             |

## Key Findings & Recommendations

| Finding                                               | Evidence                                                                              | Recommendation                                                                    |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Support در چند KPI عملیاتی مقادیر نامطلوب‌تری دارد    | Answer Rate = 82.66%, Abandon Rate = 17.34%, AWT = 142.5s, AHT = 406.21s, CSAT = 3.18 | ظرفیت پاسخگویی و فرآیند رسیدگی در Support بررسی شود.                              |
| Call Mix به‌تنهایی AHT بالای Support را توضیح نمی‌دهد | AHT در Support برای تمام Call Reasonها بالاتر از دو تیم دیگر است                      | Workflow و نحوه رسیدگی به تماس‌ها در Support بررسی شود.                           |
| Transfer با AHT بالاتر همراه است، اما علت قطعی نیست   | AHT تماس‌های Transferred = 350.87s در مقابل 301.12s برای سایر تماس‌ها                 | Routing و Knowledge Base برای Call Reasonهای دارای Transfer Rate بالا بررسی شوند. |
| بین Agentهای Support اختلاف AHT وجود دارد             | A07 با 526.62s و 29 تماس، AHT بالایی دارد                                             | Agentهای دارای AHT بالا با توجه به حجم تماس و Call Mix بررسی شوند.                |

## Dashboard

An interactive dashboard was developed using HTML, CSS, and JavaScript to visualize call center performance.

The dashboard is connected to the FastAPI backend and provides:

- KPI cards for Answer Rate, Abandon Rate, AHT, AWT, CSAT, FCR, Transfer Rate, and Contact Volume
- Filters by team, shift, and date range
- Contact volume by hour
- Contact volume by day
- Peak hour and peak day indicators

The dashboard retrieves filtered KPI results directly from the FastAPI `/kpis` endpoint.

## FastAPI

A FastAPI backend was developed to expose the calculated call center KPIs through an API.

### Available Endpoints

| Endpoint     | Description                                   |
| ------------ | --------------------------------------------- |
| `/`          | Checks whether the API is running             |
| `/data-info` | Returns the number of rows and columns        |
| `/kpis`      | Returns calculated KPIs with optional filters |

### Available Filters

The `/kpis` endpoint supports:

- `team`
- `shift`
- `start_date`
- `end_date`

Example:

```text
/kpis?team=Support&shift=Morning&start_date=2026-01-05&end_date=2026-01-15
```

### Dataset Availability

The dataset used for this project is not included in the repository because its data privacy and publication status could not be verified.

To run the project, place the provided cleaned dataset at:

`data/call_center_cleaned.csv`

The FastAPI backend loads the dataset from this path.
