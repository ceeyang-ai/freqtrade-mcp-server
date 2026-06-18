# Freqtrade MCP Server 🤖📈

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ceeyang-ai/freqtrade-mcp-server?style=flat-square)](https://github.com/ceeyang-ai/freqtrade-mcp-server)
[![MCP](https://img.shields.io/badge/MCP%20Server-5e81ac?style=flat-square)](https://github.com/ceeyang-ai/freqtrade-mcp-server)
[![GitHub](https://img.shields.io/badge/GitHub-ceeyang--ai/freqtrade--mcp--server-black?logo=github)](https://github.com/ceeyang-ai/freqtrade-mcp-server)

A **Model Context Protocol (MCP)** server for cryptocurrency trading via [Freqtrade](https://www.freqtrade.io/) — manage trades, check balances, configure strategies, backtest, and control the bot lifecycle.

> Built for AI agents. Works with **Hermes Agent**, **Claude Code**, **Cursor**, and any MCP-compatible client.

## ✨ Features

### System & Health
| Tool | Description |
|------|-------------|
| `ping` | Check if the freqtrade API server is reachable |
| `get_version` | Get the running bot version |
| `get_health` | Detailed bot health (uptime, loop time) |
| `get_logs` | Recent bot log messages |
| `get_sysinfo` | System resource usage (CPU, RAM) |

### Bot Lifecycle
| Tool | Description |
|------|-------------|
| `start_bot` | Start the trading bot |
| `stop_bot` | Stop the trading bot gracefully |
| `stop_buying` | Prevent new trades (existing sells still handled) |

### Trade Information
| Tool | Description |
|------|-------------|
| `get_open_trades` | List all open trades with P&L |
| `get_trade_detail` | Full details of a specific trade |
| `get_trade_history` | Historical closed trades with pagination |
| `get_count` | Open trade count vs max allowed |

### Account & Performance
| Tool | Description |
|------|-------------|
| `get_balance` | Full account balance across all currencies |
| `get_profit` | Profit/loss summary (total, factor, %) |
| `get_daily_profit` | Daily P&L breakdown |
| `get_weekly_profit` | Weekly P&L breakdown |
| `get_monthly_profit` | Monthly P&L breakdown |
| `get_performance` | Per-pair trade performance |

### Trading Actions
| Tool | Description |
|------|-------------|
| `force_entry` | Force-enter a trade (long/short) |
| `force_exit` | Force-exit (sell) an open trade |

### Pairs & Locks
| Tool | Description |
|------|-------------|
| `get_whitelist` | Active trading pair whitelist |
| `get_blacklist` | Blacklisted pairs |
| `add_to_blacklist` | Add pairs to blacklist |
| `get_locks` | Active pair locks |
| `lock_pair` | Lock a trading pair |
| `unlock_pair` | Remove a pair lock |

### Strategies & Market Data
| Tool | Description |
|------|-------------|
| `list_strategies` | Available strategy classes |
| `get_strategy_detail` | Strategy information |
| `get_pair_candles` | OHLCV candle data |
| `get_pair_history` | Historic analyzed data |
| `get_config` | Current bot configuration |
| `reload_config` | Reload config from disk |

## 🚀 Quick Start

```bash
# Install from GitHub
pip install git+https://github.com/ceeyang-ai/freqtrade-mcp-server.git

# Run as MCP server (connects to a running freqtrade instance)
freqtrade-mcp-server
```

### Configuration

Set the following environment variables (or use defaults):

```bash
export FREQTRADE_URL=http://127.0.0.1:8080
export FREQTRADE_USERNAME=freqtrade
export FREQTRADE_PASSWORD=your_api_password
```

## 🔌 Usage with Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  freqtrade:
    command: "freqtrade-mcp-server"
```

Restart → use `mcp_freqtrade_get_balance`, `mcp_freqtrade_force_entry`, etc.

## 🛠 Requirements

- Python 3.10+
- freqtrade-client ≥ 2026.5
- mcp ≥ 1.0
- A running [Freqtrade](https://www.freqtrade.io/) instance with REST API enabled

## 👨‍💻 Development

```bash
git clone https://github.com/ceeyang-ai/freqtrade-mcp-server.git
cd freqtrade-mcp-server
pip install -e .
freqtrade-mcp-server
```

## 📄 License

MIT — free for personal and commercial use.
