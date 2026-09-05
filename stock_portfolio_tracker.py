"""
CodeAlpha_StockPortfolioTracker
Task 2: Stock Portfolio Tracker (Advanced Version)
Concepts: dictionary, input/output, basic arithmetic, file handling, exception handling

Features:
  - Hardcoded default stock prices + option to add custom stocks
  - Profit/Loss tracking (enter your buy price vs current price)
  - Colorful terminal UI
  - Save report as .txt or .csv
"""

import os
from datetime import datetime

# ---------- Colors ----------
class C:
    HEADER = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def success(msg):
    print(f"{C.GREEN}[OK] {msg}{C.END}")


def error(msg):
    print(f"{C.RED}[ERROR] {msg}{C.END}")


def warn(msg):
    print(f"{C.YELLOW}[!] {msg}{C.END}")


def info(msg):
    print(f"{C.CYAN}{msg}{C.END}")


def section(title):
    print(f"\n{C.HEADER}{C.BOLD}--- {title} ---{C.END}")


# Hardcoded current market prices (per share)
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "AMZN": 145,
    "MSFT": 410,
    "META": 490,
    "NFLX": 650,
    "INFY": 1500,
    "TCS": 3800,
    "RELIANCE": 2900,
}


def show_available_stocks():
    print(f"\n{C.BOLD}Available Stocks (Current Price):{C.END}")
    print("-" * 32)
    print(f"{'Symbol':<10}{'Price':<10}")
    print("-" * 32)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10}{price:<10}")
    print("-" * 32)


def add_custom_stock():
    section("Add Custom Stock")
    symbol = input("Enter new stock symbol (e.g. ZOMATO): ").strip().upper()

    if not symbol:
        error("Symbol cannot be empty.")
        return

    if symbol in STOCK_PRICES:
        warn(f"'{symbol}' already exists with price {STOCK_PRICES[symbol]}.")
        if not get_yes_no("Overwrite its price? (y/n): "):
            return

    price = get_positive_float(f"Enter current price for {symbol}: ")
    if price is None:
        return

    STOCK_PRICES[symbol] = price
    success(f"'{symbol}' added at price {price}.")


def get_positive_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                warn("Price must be greater than 0.")
                continue
            return value
        except ValueError:
            warn("Invalid number. Try again (e.g. 150 or 150.50).")


def get_positive_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value <= 0:
                warn("Quantity must be a positive whole number.")
                continue
            return value
        except ValueError:
            warn("Invalid input. Please enter a whole number (e.g. 10).")


def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        warn("Please answer 'y' or 'n'.")


def get_portfolio():
    portfolio = {}  # symbol -> {"quantity": int, "buy_price": float}
    print(f"\n{C.BOLD}Enter your stock holdings.{C.END} "
          f"Type 'done' to finish, 'list' to see stocks, 'add' for a custom stock.\n")

    while True:
        symbol_input = input("Stock symbol (or 'done'/'list'/'add'): ").strip().upper()

        if symbol_input == "":
            warn("Input cannot be empty. Try again.")
            continue

        if symbol_input == "DONE":
            break

        if symbol_input == "LIST":
            show_available_stocks()
            continue

        if symbol_input == "ADD":
            add_custom_stock()
            continue

        if symbol_input not in STOCK_PRICES:
            error(f"'{symbol_input}' not found. Type 'list' to see valid symbols or 'add' to add it.")
            continue

        current_price = STOCK_PRICES[symbol_input]
        qty = get_positive_int(f"Quantity of {symbol_input}: ")

        use_current = get_yes_no(
            f"Use current price ({current_price}) as your buy price too? (y/n): "
        )
        if use_current:
            buy_price = current_price
        else:
            buy_price = get_positive_float(f"Enter your buy price per share for {symbol_input}: ")

        if symbol_input in portfolio:
            # Weighted average buy price if adding more of the same stock
            old_qty = portfolio[symbol_input]["quantity"]
            old_buy = portfolio[symbol_input]["buy_price"]
            new_qty = old_qty + qty
            new_buy = ((old_qty * old_buy) + (qty * buy_price)) / new_qty
            portfolio[symbol_input] = {"quantity": new_qty, "buy_price": round(new_buy, 2)}
        else:
            portfolio[symbol_input] = {"quantity": qty, "buy_price": buy_price}

        success(f"Added {qty} share(s) of {symbol_input}. "
                f"(Total held: {portfolio[symbol_input]['quantity']})")

    return portfolio


def calculate_investment(portfolio):
    breakdown = {}
    total_current_value = 0
    total_invested = 0

    for symbol, data in portfolio.items():
        qty = data["quantity"]
        buy_price = data["buy_price"]
        current_price = STOCK_PRICES.get(symbol, buy_price)

        invested = buy_price * qty
        current_value = current_price * qty
        profit_loss = current_value - invested
        pct_change = (profit_loss / invested * 100) if invested > 0 else 0

        breakdown[symbol] = {
            "quantity": qty,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "pct_change": pct_change,
        }

        total_invested += invested
        total_current_value += current_value

    return breakdown, total_invested, total_current_value


def display_summary(breakdown, total_invested, total_current_value):
    print("\n" + C.BOLD + C.HEADER + "=" * 78 + C.END)
    print(C.BOLD + C.HEADER + " " * 25 + "PORTFOLIO SUMMARY" + C.END)
    print(C.BOLD + C.HEADER + "=" * 78 + C.END)
    print(f"{'Stock':<9}{'Qty':<6}{'Buy':<9}{'Now':<9}{'Invested':<11}{'Value':<11}{'P/L':<11}{'P/L %':<8}")
    print("-" * 78)

    for symbol, d in sorted(breakdown.items(), key=lambda x: -x[1]["current_value"]):
        pl = d["profit_loss"]
        pl_color = C.GREEN if pl >= 0 else C.RED
        pl_sign = "+" if pl >= 0 else ""
        print(f"{symbol:<9}{d['quantity']:<6}{d['buy_price']:<9.2f}{d['current_price']:<9.2f}"
              f"{d['invested']:<11.2f}{d['current_value']:<11.2f}"
              f"{pl_color}{pl_sign}{pl:<10.2f}{pl_sign}{d['pct_change']:<6.2f}%{C.END}")

    print("-" * 78)
    total_pl = total_current_value - total_invested
    total_pl_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0
    pl_color = C.GREEN if total_pl >= 0 else C.RED
    pl_sign = "+" if total_pl >= 0 else ""

    print(f"{C.BOLD}{'TOTAL INVESTED':<30}: {total_invested:.2f}{C.END}")
    print(f"{C.BOLD}{'CURRENT VALUE':<30}: {total_current_value:.2f}{C.END}")
    print(f"{pl_color}{C.BOLD}{'TOTAL PROFIT/LOSS':<30}: {pl_sign}{total_pl:.2f} ({pl_sign}{total_pl_pct:.2f}%){C.END}")
    print(C.BOLD + C.HEADER + "=" * 78 + C.END)


def get_safe_filename(base, extension):
    filename = f"{base}.{extension}"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}.{extension}"
        counter += 1
    return filename


def save_to_file(breakdown, total_invested, total_current_value, filetype="txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = get_safe_filename(f"portfolio_report_{timestamp}", filetype)
    total_pl = total_current_value - total_invested
    total_pl_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0

    try:
        if filetype == "csv":
            with open(filename, "w", newline="") as f:
                f.write("Stock,Quantity,BuyPrice,CurrentPrice,Invested,CurrentValue,ProfitLoss,PctChange\n")
                for symbol, d in breakdown.items():
                    f.write(f"{symbol},{d['quantity']},{d['buy_price']},{d['current_price']},"
                            f"{d['invested']:.2f},{d['current_value']:.2f},"
                            f"{d['profit_loss']:.2f},{d['pct_change']:.2f}\n")
                f.write(f"TOTAL,,,,{total_invested:.2f},{total_current_value:.2f},"
                        f"{total_pl:.2f},{total_pl_pct:.2f}\n")
        else:
            with open(filename, "w") as f:
                f.write("STOCK PORTFOLIO REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 78 + "\n")
                f.write(f"{'Stock':<9}{'Qty':<6}{'Buy':<9}{'Now':<9}{'Invested':<11}"
                        f"{'Value':<11}{'P/L':<11}{'P/L %':<8}\n")
                f.write("-" * 78 + "\n")
                for symbol, d in breakdown.items():
                    sign = "+" if d["profit_loss"] >= 0 else ""
                    f.write(f"{symbol:<9}{d['quantity']:<6}{d['buy_price']:<9.2f}"
                            f"{d['current_price']:<9.2f}{d['invested']:<11.2f}"
                            f"{d['current_value']:<11.2f}{sign}{d['profit_loss']:<10.2f}"
                            f"{sign}{d['pct_change']:<6.2f}%\n")
                f.write("-" * 78 + "\n")
                sign = "+" if total_pl >= 0 else ""
                f.write(f"TOTAL INVESTED : {total_invested:.2f}\n")
                f.write(f"CURRENT VALUE  : {total_current_value:.2f}\n")
                f.write(f"PROFIT/LOSS    : {sign}{total_pl:.2f} ({sign}{total_pl_pct:.2f}%)\n")

        success(f"Report saved as: {os.path.abspath(filename)}")
        return True

    except (IOError, OSError) as e:
        error(f"Could not save file: {e}")
        return False


def main():
    print(f"{C.BOLD}{C.HEADER}" + "=" * 55 + C.END)
    print(f"{C.BOLD}{C.HEADER}" + " " * 10 + "STOCK PORTFOLIO TRACKER" + C.END)
    print(f"{C.BOLD}{C.HEADER}" + "=" * 55 + C.END)

    try:
        show_available_stocks()
        portfolio = get_portfolio()

        if not portfolio:
            warn("No stocks entered. Exiting.")
            return

        breakdown, total_invested, total_current_value = calculate_investment(portfolio)
        display_summary(breakdown, total_invested, total_current_value)

        if get_yes_no("\nSave report to file? (y/n): "):
            while True:
                fmt = input("Format - txt or csv? ").strip().lower()
                if fmt in ("txt", "csv"):
                    save_to_file(breakdown, total_invested, total_current_value, fmt)
                    break
                warn("Please type 'txt' or 'csv'.")

        info("\nThank you for using Stock Portfolio Tracker!")

    except KeyboardInterrupt:
        warn("\n\nProgram interrupted by user. Exiting safely. Goodbye!")
    except Exception as e:
        error(f"\nAn unexpected error occurred: {e}")
        info("Please restart the program.")


if __name__ == "__main__":
    main()
