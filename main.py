from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("data/call_center_cleaned.csv")


@app.get("/")
def home():
    return {"message": "Call Center API is running"}


@app.get("/data-info")
def data_info():
    return {
        "rows": len(df),
        "columns": len(df.columns)
    }


@app.get("/kpis")
def get_kpis(
    team: str | None = None,
    shift: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):

    filtered_df = df.copy()

    # Validate Team
    valid_teams = ["Support", "Sales", "Billing"]

    if team:
        if team not in valid_teams:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid team. Choose from: {valid_teams}"
            )

        filtered_df = filtered_df[
            filtered_df["queue"] == team
        ]

    # Validate Shift
    valid_shifts = ["Morning", "Evening"]

    if shift:
        if shift not in valid_shifts:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid shift. Choose from: {valid_shifts}"
            )

        filtered_df = filtered_df[
            filtered_df["shift"] == shift
        ]

    # Convert date column
    filtered_df["call_date"] = pd.to_datetime(
        filtered_df["call_date"]
    )

    # Validate Start Date
    start = None

    if start_date:
        try:
            start = pd.to_datetime(start_date)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid start_date format. Use YYYY-MM-DD."
            )

        filtered_df = filtered_df[
            filtered_df["call_date"] >= start
        ]

    # Validate End Date
    end = None

    if end_date:
        try:
            end = pd.to_datetime(end_date)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid end_date format. Use YYYY-MM-DD."
            )

        filtered_df = filtered_df[
            filtered_df["call_date"] <= end
        ]

    # Validate Date Range
    if start is not None and end is not None:
        if start > end:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be later than end_date."
            )

    # Check empty result
    if filtered_df.empty:
        raise HTTPException(
            status_code=404,
            detail="No data found for the given filters."
        )

    # Total Calls
    total_calls = len(filtered_df)

    # Answer Rate
    handled_calls = (
        filtered_df["status"]
        .isin(["Answered", "Transferred"])
        .sum()
    )

    answer_rate = (
        handled_calls / total_calls
    ) * 100

    # Abandon Rate
    abandoned_calls = (
        filtered_df["status"] == "Abandoned"
    ).sum()

    abandon_rate = (
        abandoned_calls / total_calls
    ) * 100

    # Average Wait Time
    awt = filtered_df["wait_seconds"].mean()

    # Average Handle Time
    aht = filtered_df["handle_seconds_clean"].mean()

    # Customer Satisfaction
    csat = filtered_df["csat_score"].mean()

    # First Contact Resolution
    fcr_valid = (
        filtered_df["first_contact_resolution"]
        .dropna()
    )

    fcr = (
        (fcr_valid == "Yes").mean()
    ) * 100

    # Transfer Rate
    transferred_calls = (
        filtered_df["status"] == "Transferred"
    ).sum()

    transfer_rate = (
        transferred_calls / total_calls
    ) * 100

    # Average After Call Work
    acw = (
        filtered_df["after_call_work_seconds"]
        .mean()
    )

    # Contact Volume
    contact_volume = total_calls

    # Contact Volume by Hour
    hourly_volume = (
        filtered_df["hour"]
        .value_counts()
        .sort_index()
    )

    hourly_volume = {
        str(hour): int(volume)
        for hour, volume in hourly_volume.items()
    }

    # Peak Hour
    peak_hour = (
        filtered_df["hour"]
        .value_counts()
        .idxmax()
    )

    peak_hour_volume = (
        filtered_df["hour"]
        .value_counts()
        .max()
    )

    # Contact Volume by Day
    daily_volume = (
        filtered_df["call_date"]
        .value_counts()
        .sort_index()
    )

    daily_volume = {
        day.strftime("%Y-%m-%d"): int(volume)
        for day, volume in daily_volume.items()
    }

    # Peak Day
    peak_day = (
        filtered_df["call_date"]
        .value_counts()
        .idxmax()
    )

    peak_day_volume = (
        filtered_df["call_date"]
        .value_counts()
        .max()
    )

    # Return Results
    return {
        "answer_rate": round(answer_rate, 2),
        "abandon_rate": round(abandon_rate, 2),
        "awt_seconds": round(awt, 2),
        "aht_seconds": round(aht, 2),
        "csat": round(csat, 2),
        "fcr": round(fcr, 2),

        "transfer_rate": round(transfer_rate, 2),
        "average_acw_seconds": round(acw, 2),
        "contact_volume": contact_volume,

        "contact_volume_by_hour": hourly_volume,
        "peak_hour": int(peak_hour),
        "peak_hour_volume": int(peak_hour_volume),

        "contact_volume_by_day": daily_volume,
        "peak_day": peak_day.strftime("%Y-%m-%d"),
        "peak_day_volume": int(peak_day_volume)
    }