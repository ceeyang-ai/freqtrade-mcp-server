# Freqtrade MCP Server 🤖📈

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ceeyang-ai/freqtrade-mcp-server?style=flat-square)](https://github.com/ceeyang-ai/freqtrade-mcp-server)
[![MCP](https://img.shields.io/badge/MCP-Server-5e81ac?style=flat-square)](https://modelcontextprotocol.io)
[![GitHub](https://img.shields.io/badge/GitHub-ceeyang--ai/freqtrade--mcp--server-black?logo=github)](https://github.com/ceeyang-ai/freqtrade-mcp-server)

A **Model Context Protocol (MCP)** server for cryptocurrency trading via [Freqtrade](https://www.freqtrade.io/) — manage trades, check balances, configure strategies, backtest, and control the bot lifecycle from any MCP-compatible AI agent.

> Built for AI agents. Works with **Hermes Agent**, **Claude Code**, **Cursor**, **Windsurf**, and any MCP-compatible client.

## ✨ Features (43 Tools)

### 🔧 System & Health (5 Tools)
| Tool | Description |
|------|-------------|
| `ping` | Check if the freqtrade API server is reachable |
| `get_version` | Get the running bot version string |
| `get_health` | Detailed bot health (uptime, loop time, process status) |
| `get_logs` | Fetch recent bot log messages (configurable limit) |
| `get_sysinfo` | System resource usage (CPU, RAM, uptime) |

### 🎮 Bot Lifecycle (3 Tools)
| Tool | Description |
|------|-------------|
| `start_bot` | Start the trading bot (if currently stopped) |
| `stop_bot` | Stop the trading bot gracefully |
| `stop_buying` | Temporarily prevent new trades (reload config to re-enable) |

### 📊 Trade Information (6 Tools)
| Tool | Description |
|------|-------------|
| `get_open_trades` | List all open trades with current profit/loss |
| `get_trade_detail` | Full details of a specific trade by ID |
| `get_trade_history` | Historical closed trades with pagination |
| `get_count` | Open trade count vs maximum allowed |
| `delete_trade` | Permanently delete a trade from the database |
| `cancel_open_order` | Cancel an open order for a specific trade |

### 💰 Account & Performance (10 Tools)
| Tool | Description |
|------|-------------|
| `get_balance` | Full account balance across all currencies |
| `get_profit` | Profit/loss summary (total, factor, percentage) |
| `get_daily_profit` | Daily P&L breakdown for last N days |
| `get_weekly_profit` | Weekly P&L breakdown for last N weeks |
| `get_monthly_profit` | Monthly P&L breakdown for last N months |
| `get_performance` | Per-pair trade performance (best/worst) |
| `get_stats` | Stats report (exit reasons, durations) |
| `get_entries_analysis` | Analyze trade entries by buy tag |
| `get_exits_analysis` | Analyze trade exits by exit reason |
| `get_mix_tags` | Combined entry tag + exit reason analysis |

### 🎯 Trading Actions (2 Tools)
| Tool | Description |
|------|-------------|
| `force_entry` | Force-enter a trade (long/short, with leverage & tags) |
| `force_exit` | Force-exit (sell) an open trade (partial exit supported) |

### 📋 Pairs & Whitelist/Blacklist (4 Tools)
| Tool | Description |
|------|-------------|
| `get_whitelist` | Active trading pair whitelist |
| `get_blacklist` | Currently blacklisted pairs |
| `add_to_blacklist` | Add one or more pairs to blacklist |
| `get_pairlists_available` | List available pairlist handler plugins |
| `get_available_pairs` | Pairs available for backtesting (filterable) |

### 🔒 Pair Locks (3 Tools)
| Tool | Description |
|------|-------------|
| `get_locks` | All active pair locks |
| `lock_pair` | Lock a pair (with expiration, side, reason) |
| `unlock_pair` | Remove a pair lock by ID |

### 🧠 Strategies & Market Data (4 Tools)
| Tool | Description |
|------|-------------|
| `list_strategies` | Available strategy classes |
| `get_strategy_detail` | Strategy information (code, params, timeframe) |
| `get_plot_config` | Plot configuration from active strategy |
| `get_pair_candles` | Live OHLCV candle data (any pair/timeframe) |
| `get_pair_history` | Historic analyzed dataframe for a pair + strategy |

### ⚙️ Configuration (2 Tools)
| Tool | Description |
|------|-------------|
| `get_config` | Current (sanitized) bot configuration |
| `reload_config` | Reload config from disk (no restart needed) |

### 🗃️ Custom Data (2 Tools)
| Tool | Description |
|------|-------------|
| `get_custom_data` | Custom data stored for a specific trade |
| `get_open_trades_custom_data` | Custom data across all open trades |

## 🚀 Quick Start

### 1. Install

```bash
pip install git+https://github.com/ceeyang-ai/freqtrade-mcp-server.git
```

### 2. Start Freqtrade (dry-run for testing)

Create a minimal config (`config.json`):

```json
{
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "stake_amount": 50,
    "dry_run": true,
    "dry_run_wallet": 1000,
    "timeframe": "5m",
    "exchange": {
        "name": "binance",
        "pair_whitelist": ["BTC/USDT", "ETH/USDT"]
    },
    "api_server": {
        "enabled": true,
        "listen_port": 8080,
        "username": "freqtrader",
        "password": "your_password",
        "jwt_secret_key": "a-very-long-random-string-at-least-32-chars"
    }
}
```

```bash
freqtrade trade --strategy SampleStrategy --config config.json
```

### 3. Run the MCP Server

```bash
export FREQTRADE_URL=http://127.0.0.1:8080
export FREQTRADE_USERNAME=freqtrader
export FREQTRADE_PASSWORD=your_password

freqtrade-mcp-server
```

### Configuration via Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FREQTRADE_URL` | No | `http://127.0.0.1:8080` | Freqtrade API server URL |
| `FREQTRADE_USERNAME` | No | `freqtrade` | API username from `api_server` config |
| `FREQTRADE_PASSWORD` | No | `""` | API password from `api_server` config |

## 🔌 Usage with AI Agents

### Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  freqtrade:
    command: "freqtrade-mcp-server"
    env:
      FREQTRADE_URL: "http://127.0.0.1:8080"
      FREQTRADE_USERNAME: "freqtrader"
      FREQTRADE_PASSWORD: "your_password"
```

Then ask your agent: *"What's my current crypto portfolio balance?"*, *"Force-enter BTC/USDT long"*, *"Run a backtest on BTC/USDT"*

### Claude Code / Cursor

```json
{
  "mcpServers": {
    "freqtrade": {
      "command": "freqtrade-mcp-server",
      "env": {
        "FREQTRADE_URL": "http://127.0.0.1:8080",
        "FREQTRADE_USERNAME": "freqtrader",
        "FREQTRADE_PASSWORD": "your_password"
      }
    }
  }
}
```

## 🛠 Requirements

- **Python 3.10+**
- **Freqtrade** instance running with API server enabled (`api_server.enabled: true`)
- `freqtrade-client >= 2026.5` (installed automatically)
- `mcp >= 1.0` (installed automatically)

## 🧪 Development

```bash
git clone https://github.com/ceeyang-ai/freqtrade-mcp-server.git
cd freqtrade-mcp-server
pip install -e .

# Run integration tests (requires running Freqtrade instance)
python test_integration.py
```

## 🤝 Related Projects

- [**doc-mcp-server**](https://github.com/ceeyang-ai/doc-mcp-server) — Document processing (PDF, text conversion)
- [**viz-mcp-server**](https://github.com/ceeyang-ai/viz-mcp-server) — Data visualization (matplotlib/seaborn charts)
- [**webx-mcp-server**](https://github.com/ceeyang-ai/webx-mcp-server) — Web page extraction and conversion

## 📄 License

MIT — free for personal and commercial use.
