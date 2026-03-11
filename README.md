# moomoo_trade_bot 🤖📈

A high-performance algorithmic trading bot for Moomoo, built with **OpenCode** and designed for **Raspberry Pi 4** and **GCP VM** environments.

## 🚀 AI-Powered Development

This project utilizes **OpenCode Superpowers** to ensure robust code quality and strategy execution.

### Superpower Skills Used:
- **/superpowers:brainstorm** - Used to define risk parameters and strategy logic.
- **/superpowers:write-plan** - Created the architectural roadmap for the bot.
- **/superpowers:execute-plan** - Automated the generation of the API boilerplate and test suites.

---

## 🛠 Prerequisites

### 1. Moomoo OpenD Gateway

Moomoo requires a local gateway to bridge the API and their servers.

- **Download:** [Moomoo OpenAPI v10.0](https://openapi.moomoo.com/moomoo-api-doc/en/)
- **Configuration:** Ensure OpenD is running on `127.0.0.1` at port `11111`.

### 2. Environment Setup

```bash
# Clone this repo
git clone https://github.com/clawzhao/moomoo_trade_bot.git
cd moomoo_trade_bot

# Install dependencies
pip install moomoo-api pandas
```

### 3. Please always use tradebot_todo.md to track the progress.

## 🧪 End-to-End (E2E) Test

Before running any live strategy, verify your connection to the Paper Trading (Simulation) environment.

## 📂 Project Structure

- `strategy/`: AI-generated trading logic (e.g., SMA, RSI).
- `tests/`: TDD test suite to prevent capital loss.
- `utils/`: Logging and Telegram notification helpers.
- `config.json`: Store your Account IDs and API preferences.

## ⚠️ Important Safety Note

This bot is strictly configured for Simulation/Paper Trading by default. Do not switch to `TrdEnv.REAL` until you have completed at least 100 successful simulated trades.
