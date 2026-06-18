"""freqtrade-mcp-server: Freqtrade Trading MCP Server v0.1.0

Provides cryptocurrency trading operations via MCP protocol:
- Full trading lifecycle: start/stop, force enter/exit
- Account info: balance, profit, performance
- Data: backtesting, strategy listing, pair management
- System: health check, logs, config

Requires a running freqtrade instance with API server enabled.
"""

import json
from mcp.server.fastmcp import FastMCP
from freqtrade_client import FtRestClient

mcp = FastMCP("freqtrade-mcp-server")


def _client() -> FtRestClient:
    """Return an FtRestClient connected to the local freqtrade instance."""
    return FtRestClient("http://127.0.0.1:8080", "freqtrader", "trading123")


def _ok(data) -> str:
    return json.dumps({"success": True, "data": data}, default=str)


def _err(msg: str) -> str:
    return json.dumps({"success": False, "error": msg})


# ─── System ──────────────────────────────────────────────────────────


@mcp.tool()
def ping() -> str:
    """Check if the freqtrade API server is reachable."""
    try:
        r = _client()._get("ping")
        return _ok(r)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_version() -> str:
    """Get freqtrade bot version."""
    try:
        return _ok(_client().version())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_health() -> str:
    """Get bot health status (last loop time, etc.)."""
    try:
        return _ok(_client().health())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_logs(limit: int = 50) -> str:
    """Get recent log messages.

    Args:
        limit: Number of log lines to return (default 50, max 200)
    """
    try:
        limit = min(limit, 200)
        r = _client()._get("logs", params={"limit": limit})
        # Format logs for readability
        logs = r.get("logs", r) if isinstance(r, dict) else r
        return _ok(logs)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_sysinfo() -> str:
    """Get system information (CPU, RAM usage)."""
    try:
        return _ok(_client().sysinfo())
    except Exception as e:
        return _err(str(e))


# ─── Trading Control ────────────────────────────────────────────────


@mcp.tool()
def start_trading() -> str:
    """Start the trading bot."""
    try:
        return _ok(_client().start())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def stop_trading() -> str:
    """Stop the trading bot."""
    try:
        return _ok(_client().stop())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_trading_status() -> str:
    """Get current bot state (running/stopped/paused)."""
    try:
        # FtRestClient doesn't have a dedicated status endpoint
        # but /ping and /health give us info
        ping_r = _client()._get("ping")
        return _ok({"ping": ping_r})
    except Exception as e:
        return _err(str(e))


# ─── Trade Information ──────────────────────────────────────────────


@mcp.tool()
def get_open_trades() -> str:
    """Get all currently open trades."""
    try:
        trader = _client()
        status = trader.status()
        if isinstance(status, list):
            return _ok({"count": len(status), "trades": status})
        return _ok({"count": 0, "trades": []})
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_trade_detail(trade_id: int) -> str:
    """Get details of a specific trade by its ID.

    Args:
        trade_id: The trade ID to look up
    """
    try:
        return _ok(_client()._get(f"trade/{trade_id}"))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_trade_history(limit: int = 20, offset: int = 0) -> str:
    """Get trade history (closed trades).

    Args:
        limit: Number of trades to return (default 20, max 100)
        offset: Pagination offset
    """
    try:
        limit = min(limit, 100)
        r = _client()._get("trades", params={"limit": limit, "offset": offset})
        return _ok(r)
    except Exception as e:
        return _err(str(e))


# ─── Account / Performance ──────────────────────────────────────────


@mcp.tool()
def get_balance() -> str:
    """Get account balance (all currencies)."""
    try:
        return _ok(_client().balance())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_profit() -> str:
    """Get profit/loss summary."""
    try:
        return _ok(_client().profit())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_daily_profit(days: int = 7) -> str:
    """Get daily profit breakdown.

    Args:
        days: Number of days (default 7, max 365)
    """
    try:
        days = min(days, 365)
        return _ok(_client().daily(days))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_performance() -> str:
    """Get per-pair trade performance."""
    try:
        return _ok(_client().performance())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_count() -> str:
    """Get open trade count vs maximum."""
    try:
        return _ok(_client().count())
    except Exception as e:
        return _err(str(e))


# ─── Trading Actions ────────────────────────────────────────────────


@mcp.tool()
def force_entry(
    pair: str,
    side: str = "long",
    stake_amount: float | None = None,
) -> str:
    """Force-enter a trade.

    Args:
        pair: Trading pair (e.g. 'BTC/USDT')
        side: 'long' or 'short'
        stake_amount: Optional stake amount override (uses config default if omitted)
    """
    try:
        payload = {"pair": pair, "side": side.upper()}
        if stake_amount is not None:
            payload["stake_amount"] = stake_amount
        r = _client()._post("forceenter", data=payload)
        return _ok(r)
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def force_exit(trade_id: int, amount: float | None = None) -> str:
    """Force-exit a trade.

    Args:
        trade_id: ID of the trade to exit
        amount: Optional partial exit amount
    """
    try:
        payload = {"tradeid": trade_id}
        if amount is not None:
            payload["amount"] = amount
        r = _client()._post("forceexit", data=payload)
        return _ok(r)
    except Exception as e:
        return _err(str(e))


# ─── Pair Management ────────────────────────────────────────────────


@mcp.tool()
def get_whitelist() -> str:
    """Get current trading pair whitelist."""
    try:
        return _ok(_client().whitelist())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def get_blacklist() -> str:
    """Get current blacklisted pairs."""
    try:
        return _ok(_client().blacklist())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def add_to_blacklist(pairs: list[str]) -> str:
    """Add pairs to the blacklist.

    Args:
        pairs: List of trading pairs to blacklist (e.g. ['DOGE/USDT', 'SHIB/USDT'])
    """
    try:
        return _ok(_client()._post("blacklist", data={"blacklist": pairs}))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def delete_from_blacklist(pairs: list[str]) -> str:
    """Remove pairs from the blacklist.

    Args:
        pairs: List of trading pairs to remove from blacklist
    """
    try:
        r = _client()._delete("blacklist", data={"blacklist": pairs})
        return _ok(r)
    except Exception as e:
        return _err(str(e))


# ─── Backtesting ────────────────────────────────────────────────────


@mcp.tool()
def list_strategies() -> str:
    """List all available trading strategies."""
    try:
        r = _client()._get("strategies")
        strategies = r.get("strategies", r) if isinstance(r, dict) else r
        return _ok({"count": len(strategies) if isinstance(strategies, list) else 0,
                     "strategies": strategies})
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def list_exchanges() -> str:
    """List supported exchanges."""
    try:
        return _ok(_client()._get("exchanges"))
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def run_backtest(
    strategy: str,
    timerange: str,
    timeframe: str = "5m",
    max_open_trades: int = 3,
) -> str:
    """Run a backtest using the webserver endpoint.

    Note: Requires freqtrade to be running in webserver mode or
    with webserver endpoints enabled.

    Args:
        strategy: Strategy class name
        timerange: Time range (e.g. '20240101-20240601' or '30d')
        timeframe: Candle timeframe (default '5m')
        max_open_trades: Max concurrent trades
    """
    try:
        payload = {
            "strategy": strategy,
            "timerange": timerange,
            "timeframe": timeframe,
            "max_open_trades": max_open_trades,
        }
        r = _client()._post("backtest", data=payload)
        return _ok(r)
    except Exception as e:
        return _err(str(e))


# ─── Config / Reload ────────────────────────────────────────────────


@mcp.tool()
def get_config() -> str:
    """Get the current (sanitized) bot configuration."""
    try:
        return _ok(_client().show_config())
    except Exception as e:
        return _err(str(e))


@mcp.tool()
def reload_config() -> str:
    """Reload configuration from disk."""
    try:
        return _ok(_client().reload_config())
    except Exception as e:
        return _err(str(e))


# ─── Entry Point ───────────────────────────────────────────────────────


def main():
    mcp.run()


if __name__ == "__main__":
    main()
