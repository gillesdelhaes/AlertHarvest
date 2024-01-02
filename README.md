# AlertHarvest
A monitoring software

Setup:
docker compose -up -d 

URL:
Dashboard link : http://127.0.0.1:8000/viz/dashboard/

Push new alerts using api :
http://127.0.0.1:8000/api/create_alert/
POST request
json body example

{
    "timestamp": "2024-01-03 07:30:10",
    "location": "Demo",
    "severity": "CRITICAL",
    "message": "Unexplained voltage fluctuations",
    "source": "Grid Monitoring"
}

For notifications, create rules following examples.
Create modules following example.
Discord module active and running.

If you need more info or want to contribute https://discord.gg/hduVhv7VaA
