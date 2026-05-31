# Prompt Log - Week 5 Session A Lab 1

**Student:** Mahmudul Hasan (4125999049)
**Lab:** Rainfall Forecasting and Alert System

## API integration

**Field:** rain.1h (mm/h); missing rain -> 0 mm
**Endpoint:** api.openweathermap.org/data/2.5/weather
**Cities tested:** Dhaka, Beijing, Delhi, Moscow, Islamabad (all GREEN, 0 mm/h)
**401:** Key not active initially; OPENWEATHER_API_KEY=bad -> 401 after fix

## Alerts

GREEN < 10 | YELLOW 10-20 | RED > 20 mm/h
History: data/alert_history.csv (5 rows)

## Dashboard

python3 -m streamlit run dashboard.py -> localhost:8501

## Lessons learned

Export API key only in terminal; activation delay common; terminal screenshot documents 401 then success.
