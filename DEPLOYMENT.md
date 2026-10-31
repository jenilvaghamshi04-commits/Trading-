# Render web service

- Repository: jenilvaghamshi04-commits/Trading-
- Branch: main
- Runtime: Python 3
- Root Directory: leave empty
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`
- Health Check Path: `/health`

Deploy the latest commit after saving these settings. The process binds to
0.0.0.0 and Render's PORT environment variable (10000 locally).

The web home lists the eleven original modules, shows their documentation and
CLI help commands, and provides a browser-only long-position sizing calculator.
The dedicated `/scanner` page explains scan modes, setup rules, coverage and
session timing, with a validated command builder and the complete scanner reference.
It does not run scans, stream prices, schedule alerts, connect to a brokerage,
or place trades through the browser. The original Python tools are included
unchanged and can be run locally using the README instructions.

To run locally: `python app.py`, then open http://localhost:10000.
