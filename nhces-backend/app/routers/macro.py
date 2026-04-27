import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.database import get_db
from app.schemas.macro import MacroSnapshot, MacroVariable, MacroHistory, MacroHistoryPoint

logger = logging.getLogger(__name__)
router = APIRouter()

# Metadata for each macro variable
_META = {
    "ngn_usd":          ("NGN/USD Exchange Rate",   "NGN per USD",      "macro_fx",       "ngn_usd"),
    "ngn_eur":          ("NGN/EUR Exchange Rate",   "NGN per EUR",      "macro_fx",       "ngn_eur"),
    "ngn_gbp":          ("NGN/GBP Exchange Rate",   "NGN per GBP",      "macro_fx",       "ngn_gbp"),
    "cpi_annual_pct":   ("CPI Inflation (Annual)",  "% per annum",      "macro_cpi",      "cpi_annual_pct"),
    "gdp_growth_pct":   ("GDP Growth Rate",         "% per annum",      "macro_gdp",      "gdp_growth_pct"),
    "lending_rate_pct": ("Lending Interest Rate",   "% per annum",      "macro_interest", "lending_rate_pct"),
    "brent_usd_barrel": ("Brent Crude Oil Price",   "USD per barrel",   "macro_oil",      "brent_usd_barrel"),
}


def _freshness_level(rows: list[dict]) -> str:
    """Return worst data_level across a set of DB rows."""
    levels = {r.get("data_level", "RED") for r in rows if r}
    if "RED"   in levels: return "RED"
    if "AMBER" in levels: return "AMBER"
    return "GREEN"


@router.get("", response_model=MacroSnapshot)
async def get_macro_snapshot():
    """
    Latest macroeconomic snapshot — one value per variable.
    Used by the dashboard MacroSnapshot card.
    """
    db = get_db()
    variables: list[MacroVariable] = []
    all_rows: list[dict] = []

    for var_key, (label, unit, table, col) in _META.items():
        try:
            resp = (
                db.table(table)
                .select(f"date,{col},source,data_level")
                .order("date", desc=True)
                .limit(1)
                .execute()
            )
            row = resp.data[0] if resp.data else None
        except Exception as e:
            logger.warning(f"[macro] Failed to fetch {table}.{col}: {e}")
            row = None

        if row:
            all_rows.append(row)
            variables.append(MacroVariable(
                variable=var_key,
                label=label,
                value=float(row[col]),
                unit=unit,
                as_of_date=str(row["date"]),
                source=row.get("source", "Unknown"),
                data_level=row.get("data_level", "RED"),
            ))
        else:
            # No data in DB — synthetic placeholder
            variables.append(MacroVariable(
                variable=var_key,
                label=label,
                value=0.0,
                unit=unit,
                as_of_date=None,
                source="No data",
                data_level="RED",
            ))

    return MacroSnapshot(
        variables=variables,
        overall_freshness=_freshness_level(all_rows),
        as_of=datetime.now(timezone.utc),
    )


@router.get("/history", response_model=MacroHistory)
async def get_macro_history(
    variable: str = Query(..., description="e.g. ngn_usd, cpi_annual_pct"),
    years:    int = Query(5, ge=1, le=25),
):
    """
    Historical series for a single macro variable.
    Used by the Macro Data page line chart.
    """
    if variable not in _META:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown variable '{variable}'. "
                   f"Valid: {', '.join(_META.keys())}",
        )

    label, unit, table, col = _META[variable]
    db = get_db()

    try:
        resp = (
            db.table(table)
            .select(f"date,{col},data_level")
            .order("date", desc=True)
            .limit(years)
            .execute()
        )
        rows = sorted(resp.data, key=lambda r: r["date"])
    except Exception as e:
        logger.warning(f"[macro/history] DB error: {e}")
        rows = []

    data_level = _freshness_level(rows) if rows else "RED"
    points = [
        MacroHistoryPoint(
            year=int(r["date"][:4]),
            value=float(r[col]),
        )
        for r in rows if r.get(col) is not None
    ]

    return MacroHistory(
        variable=variable,
        label=label,
        unit=unit,
        data_level=data_level,
        data=points,
    )
