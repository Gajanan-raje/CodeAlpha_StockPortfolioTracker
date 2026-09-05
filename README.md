
# CodeAlpha_StockPortfolioTracker

A **Stock Portfolio Tracker** built in Python as part of the CodeAlpha Python Programming Internship (Task 2).

## About
Tracks your stock holdings, calculates total investment, and shows profit or loss based on the difference between your buy price and the current price.

## Features
- 📊 10 pre-loaded stocks (AAPL, TSLA, GOOGL, TCS, RELIANCE, etc.) with current prices
- ➕ **Add custom stocks** with your own price
- 💰 **Profit/Loss tracking** — compares your buy price vs current price
- 📈 Shows profit/loss in both ₹/$ amount **and percentage (%)**
- 🎨 Colorful terminal output (green = profit, red = loss)
- 📁 Save full report as `.txt` or `.csv` file

## How Profit % is Calculated
For each stock:
```
Invested Amount   = Buy Price × Quantity
Current Value     = Current Price × Quantity
Profit/Loss (₹)   = Current Value − Invested Amount
Profit/Loss (%)   = (Profit/Loss ÷ Invested Amount) × 100
```

**Example:**
- You bought 10 shares of AAPL at ₹150 (Buy Price) → Invested = ₹1500
- Current price is ₹180 → Current Value = ₹1800
- Profit = ₹1800 − ₹1500 = **₹300**
- Profit % = (300 ÷ 1500) × 100 = **+20%**

The program shows this automatically in a table, plus a grand total for your whole portfolio.

## How to Run
```bash
python stock_portfolio_tracker.py
```

## How to Use
1. Enter a stock symbol (or type `list` to see options, `add` for a custom stock)
2. Enter quantity
3. Choose whether your buy price is same as current price, or enter your own
4. Type `done` when finished
5. View the full profit/loss summary
6. Optionally save the report as `.txt` or `.csv`

## Concepts Used
Dictionaries, input/output, arithmetic operations, file handling, exception handling

## Tech Stack
- Python 3

## Author
Gajanan Harinarayan Raje — CodeAlpha Python Programming Intern
