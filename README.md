# Weather vs Humans: Mumbai

How much of Mumbai's PM2.5 is weather, and how much is us?

Entry for the **Most Creative Submission** prize, Google Mumbai Data Challenge: Air Quality Mapping & Forecasting (Zindi, 2026).

**Live page:** https://hark.com/site/999fcb75-0471-48a0-b2a7-e25abdd8ce35?hark_region=us (also served from `docs/` via GitHub Pages)

## The idea
A LightGBM model learns PM2.5 from weather only (wind, boundary-layer height, rain, temperature, humidity), plus station and hour. Whatever it cannot explain is the human-made extra: traffic, dust, burning, firecrackers.

## Findings
- **GRAP-4 worked.** After BMC enforced GRAP-4 on 27 Nov 2025, actual PM2.5 at the 4 challenge stations fell 100.8 → 62.9 µg/m³ (12 days before vs after) while weather-expected stayed 47.4 → 47.9. 0 of 358 placebo winter windows dropped as much.
- **Diwali is getting worse.** Human extra (±2 days): 2019 +7.1, 2024 +23.6, 2025 +44.8 µg/m³/day.
- **Most bad days are human-made.** Days over 60 µg/m³ that weather alone would not explain (Feb 2025 – Oct 2026): Shivaji Nagar 56/61, Borivali East 50/56, Malad West 38/46, Byculla 39/43.

## Repo
- `docs/` – the interactive page (GitHub Pages)
- `analysis/` – model and event-test scripts, Colab notebook, weekly series
- `report/` – 2-page PDF and charts

## Data
Zindi challenge data (CPCB, CC-BY-SA 4.0), public CPCB/MPCB station history, Open-Meteo ERA5 reanalysis weather. Raw data is not redistributed here; the notebook downloads it.

## Limits
City daily R² ≈ 0.57, so the residual also holds model error. Station counts differ by year. Cigarette equivalents (≈22 µg/m³/day per cigarette, Berkeley Earth) are approximate.

Open-source tools only. Author: Aaryan Singh.
