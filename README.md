## Daily Telegram Message

Sends "Day N." (day of the year) to a Telegram chat every day via GitHub Actions.

### Setup
1. Add repo secrets: `TG_BOT_TOKEN` and `TG_CHAT_ID`.
2. Run the workflow once from the Actions tab to test.

Runs daily at 00:05 UTC (edit the cron in `.github/workflows/daily.yml`).
