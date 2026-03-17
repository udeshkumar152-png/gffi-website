name: Hourly GFFI Live Update

on:
  schedule:
    - cron: '*/60 * * * *'  # Runs every 60 minutes
  workflow_dispatch:          # Allows manual trigger

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  update-gffi-data:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: 📥 Checkout repository
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: 📦 Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas numpy pandas-datareader requests

      - name: 🔄 Run GFFI Live Calculator
        env:
          FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
          ALPHA_VANTAGE_KEY: ${{ secrets.ALPHA_VANTAGE_KEY }}
        run: python gffi_live_calculator.py

      - name: 💾 Commit and push changes
        run: |
          git config --global user.name 'GFFI Bot'
          git config --global user.email 'gffi-bot@users.noreply.github.com'
          git add data.js
          if git diff --quiet && git diff --staged --quiet; then
            echo "✅ No changes to commit"
          else
            git commit -m "🤖 Live GFFI update - $(date +'%Y-%m-%d %H:%M')"
            git pull --rebase origin main
            git push origin main
          fi

      - name: 📊 Show summary
        run: |
          echo "✅ GFFI Update Completed!"
          echo "📅 Time: $(date)"
          if [ -f data.js ]; then
            echo "📁 data.js updated successfully"
            LINES=$(wc -l < data.js)
            echo "📄 File size: $LINES lines"
          else
            echo "❌ data.js not found"
          fi
