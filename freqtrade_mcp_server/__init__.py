"""freqtrade-mcp-server: Freqtrade Trading MCP Server v0.1.0

Provides cryptocurrency trading operations via MCP protocol:
- Account: balance, profit, performance, daily/monthly/weekly breakdowns
- Trades: open trades, history, force enter/exit
- Pairs: whitelist, blacklist, lock management
- Strategies: list, details, backtesting
- Data: candle data, pair history
- Config: show/reload
- Bot lifecycle: start/stop/stopbuy
- System: health, ping, version, logs, sysinfo

Configuration via environment variables:
  FREQTRADE_URL      - API server URL (default: http://127.0.0.1:8080)
  FREQTRADE_USERNAME - API username   (default: freqtrade)
  FREQTRADE_PASSWORD - API password   (default: "")
"""

import json
import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from freqtrade_client import FtRestClient

mcp = FastMCP("freqtrade-mcp-server")

# ─── Configuration ──────────────────────────────────────────────────────

_DEFAULT_URL = os.environ.get("FREQTRADE_URL", "http://127.0.0.1:8080")
_DEFAULT_USER = os.environ.get("FREQTRADE_USERNAME", "freqtrade")
_DEFAULT_PASS = os.environ.get("FREQTRADE_PASSWORD", "")


def _client() -> FtRestClient:
    """Return an FtRestClient connected to the configured freqtrade instance."""
    return FtRestClient(_DEFAULT_URL, _DEFAULT_USER, _DEFAULT_PASS)


def _ok(data: Any) -> str:
    return json.dumps({"success": True, "data": data}, default=str, ensure_ascii=False)


def _err(msg: str) -> str:
    return json.dumps({"success": False, "error": msg})


def _safe_client_call(method_name: str, *args, **kwargs) -> str:
    """Wrap any FtRestClient method call with consistent error handling."""
    try:
        method = getattr(_client(), method_name, None)
        if method is None:
            return _err(f"Unknown method: {method_name}")
        result = method(*args, **kwargs)
        return _ok(result)
    except Exception as e:
        return _err(f"{method_name} failed: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 1. System / Health
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def ping() -> str:
    """Check if the freqtrade API server is reachable (simple health check)."""
    return _safe_client_call("ping")


@mcp.tool()
def get_version() -> str:
    """Get the running freqtrade bot version string."""
    return _safe_client_call("version")


@mcp.tool()
def get_health() -> str:
    """Get detailed bot health status (last loop time, process uptime, etc.)."""
    return _safe_client_call("health")


@mcp.tool()
def get_logs(limit: int = 50) -> str:
    """Fetch the most recent log messages from the freqtrade instance.

    Args:
        limit: Number of log lines to return (default 50, max 500).
    """
    limit = min(limit, 500)
    return _safe_client_call("logs", limit)


@mcp.tool()
def get_sysinfo() -> str:
    """Get system resource usage (CPU, RAM, uptime) from the bot host."""
    return _safe_client_call("sysinfo")


# ═══════════════════════════════════════════════════════════════════════
# 2. Bot Lifecycle Control
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def start_bot() -> str:
    """Start the freqtrade trading bot (if currently stopped)."""
    return _safe_client_call("start")


@mcp.tool()
def stop_bot() -> str:
    """Stop the freqtrade trading bot gracefully."""
    return _safe_client_call("stop")


@mcp.tool()
def stop_buying() -> str:
    """Temporarily prevent new trades from opening (existing sells still handled).
    Use `reload_config` to re-enable buying.
    """
    return _safe_client_call("stopbuy")


# ═══════════════════════════════════════════════════════════════════════
# 3. Trade Information
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_open_trades() -> str:
    """List all currently open trades with current profit/loss."""
    return _safe_client_call("status")


@mcp.tool()
def get_count() -> str:
    """Get the number of open trades vs the maximum allowed."""
    return _safe_client_call("count")


@mcp.tool()
def get_trade_detail(trade_id: int) -> str:
    """Get full details of a specific trade by its ID.

    Args:
        trade_id: The numeric trade ID.
    """
    return _safe_client_call("trade", trade_id)


@mcp.tool()
def get_trade_history(limit: int = 20, offset: int = 0, order_by_id: bool = True) -> str:
    """Get historical (closed) trades with pagination.

    Args:
        limit: Number of trades to return (default 20, max 200).
        offset: Pagination offset.
        order_by_id: Sort by trade ID (default True; False = sort by timestamp).
    """
    limit = min(limit, 200)
    return _safe_client_call("trades", limit, offset, order_by_id)


@mcp.tool()
def delete_trade(trade_id: int) -> str:
    """Permanently delete a trade from the database.

    Args:
        trade_id: The numeric trade ID to delete.
    """
    return _safe_client_call("delete_trade", trade_id)


@mcp.tool()
def cancel_open_order(trade_id: int) -> str:
    """Cancel an open order for a specific trade.

    Args:
        trade_id: The trade with the open order to cancel.
    """
    return _safe_client_call("cancel_open_order", trade_id)


# ═══════════════════════════════════════════════════════════════════════
# 4. Account / Balance / Performance
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_balance() -> str:
    """Get the full account balance across all currencies."""
    return _safe_client_call("balance")


@mcp.tool()
def get_profit() -> str:
    """Get the profit/loss summary (total, factor, percentage, etc.)."""
    return _safe_client_call("profit")


@mcp.tool()
def get_daily_profit(days: int = 7) -> str:
    """Get daily profit/loss breakdown for the last N days.

    Args:
        days: Number of days (default 7, max 365).
    """
    days = min(days, 365)
    return _safe_client_call("daily", days)


@mcp.tool()
def get_weekly_profit(weeks: int = 4) -> str:
    """Get weekly profit/loss breakdown for the last N weeks.

    Args:
        weeks: Number of weeks (default 4, max 52).
    """
    weeks = min(weeks, 52)
    return _safe_client_call("weekly", weeks)


@mcp.tool()
def get_monthly_profit(months: int = 6) -> str:
    """Get monthly profit/loss breakdown for the last N months.

    Args:
        months: Number of months (default 6, max 24).
    """
    months = min(months, 24)
    return _safe_client_call("monthly", months)


@mcp.tool()
def get_performance() -> str:
    """Get per-pair trade performance (best/worst performers)."""
    return _safe_client_call("performance")


@mcp.tool()
def get_stats() -> str:
    """Get the stats report (exit reasons, durations, etc.)."""
    return _safe_client_call("stats")


@mcp.tool()
def get_entries_analysis(pair: str = None) -> str:
    """Analyze trade entries by buy tag.

    Args:
        pair: Optional pair filter (e.g. 'BTC/USDT'). Returns all if omitted.
    """
    return _safe_client_call("entries", pair)


@mcp.tool()
def get_exits_analysis(pair: str = None) -> str:
    """Analyze trade exits by exit reason.

    Args:
        pair: Optional pair filter. Returns all if omitted.
    """
    return _safe_client_call("exits", pair)


@mcp.tool()
def get_mix_tags(pair: str = None) -> str:
    """Analyze trades by entry tag combined with exit reason.

    Args:
        pair: Optional pair filter. Returns all if omitted.
    """
    return _safe_client_call("mix_tags", pair)


# ═══════════════════════════════════════════════════════════════════════
# 5. Trading Actions
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def force_entry(
    pair: str,
    side: str = "long",
    stake_amount: float | None = None,
    leverage: float | None = None,
    enter_tag: str | None = None,
) -> str:
    """Force-enter a trade for a specific pair.

    Args:
        pair: Trading pair symbol (e.g. 'BTC/USDT').
        side: 'long' or 'short' (default 'long').
        stake_amount: Optional stake amount override. Uses config default if omitted.
        leverage: Optional leverage override.
        enter_tag: Optional tag to label this entry.
    """
    return _safe_client_call("forceenter", pair, side, stake_amount=stake_amount,
                             leverage=leverage, enter_tag=enter_tag)


@mcp.tool()
def force_exit(trade_id: int, ordertype: str | None = None,
               amount: float | None = None) -> str:
    """Force-exit (sell) an open trade.

    Args:
        trade_id: ID of the trade to exit.
        ordertype: Optional order type override (e.g. 'limit', 'market').
        amount: Optional partial exit amount.
    """
    return _safe_client_call("forceexit", trade_id, ordertype=ordertype, amount=amount)


# ═══════════════════════════════════════════════════════════════════════
# 6. Pairs & Whitelist / Blacklist
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_whitelist() -> str:
    """Get the currently active trading pair whitelist."""
    return _safe_client_call("whitelist")


@mcp.tool()
def get_blacklist() -> str:
    """Get the currently blacklisted trading pairs."""
    return _safe_client_call("blacklist")


@mcp.tool()
def add_to_blacklist(pairs: list[str]) -> str:
    """Add one or more pairs to the blacklist.

    Args:
        pairs: List of trading pair symbols to blacklist (e.g. ['DOGE/USDT']).
    """
    return _safe_client_call("blacklist", pairs)


@mcp.tool()
def get_pairlists_available() -> str:
    """List the available pairlist handler plugins."""
    return _safe_client_call("pairlists_available")


@mcp.tool()
def get_available_pairs(timeframe: str | None = None,
                        stake_currency: str | None = None) -> str:
    """Get pairs available for backtesting based on available data.

    Args:
        timeframe: Candle timeframe filter (e.g. '5m', '1h').
        stake_currency: Currency filter (e.g. 'USDT', 'BTC').
    """
    return _safe_client_call("available_pairs", timeframe, stake_currency)


# ═══════════════════════════════════════════════════════════════════════
# 7. Locks (Pair Locking)
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_locks() -> str:
    """Get all currently active pair locks."""
    return _safe_client_call("locks")


@mcp.tool()
def lock_pair(pair: str, until: str, side: str = "*", reason: str = "") -> str:
    """Lock a trading pair so the bot won't trade it.

    Args:
        pair: Pair to lock (e.g. 'BTC/USDT').
        until: Lock expiration (ISO datetime, e.g. '2026-07-01T00:00:00Z').
        side: Side to lock ('long', 'short', or '*' for both).
        reason: Optional reason for the lock.
    """
    return _safe_client_call("lock_add", pair, until, side, reason)


@mcp.tool()
def unlock_pair(lock_id: int) -> str:
    """Remove a pair lock by its ID.

    Args:
        lock_id: The lock ID to release.
    """
    return _safe_client_call("delete_lock", lock_id)


# ═══════════════════════════════════════════════════════════════════════
# 8. Strategies & Backtesting
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def list_strategies() -> str:
    """List all available trading strategy classes."""
    return _safe_client_call("strategies")


@mcp.tool()
def get_strategy_detail(strategy: str) -> str:
    """Get detailed information about a specific strategy.

    Args:
        strategy: The strategy class name.
    """
    return _safe_client_call("strategy", strategy)


@mcp.tool()
def get_plot_config() -> str:
    """Get the plot configuration defined by the active strategy."""
    return _safe_client_call("plot_config")


# ═══════════════════════════════════════════════════════════════════════
# 9. Market Data & Candle/Pair Data
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_pair_candles(pair: str, timeframe: str,
                     limit: int = 150, columns: str | None = None) -> str:
    """Fetch live OHLCV candle data for a trading pair.

    Args:
        pair: Trading pair (e.g. 'BTC/USDT').
        timeframe: Candle size (e.g. '5m', '1h', '4h', '1d').
        limit: Number of candles to return (default 150, max 500).
        columns: Optional comma-separated column filter (e.g. 'date,open,high,low,close,volume').
    """
    limit = min(limit, 500)
    return _safe_client_call("pair_candles", pair, timeframe, limit, columns)


@mcp.tool()
def get_pair_history(pair: str, timeframe: str, strategy: str,
                     timerange: str | None = None,
                     freqaimodel: str | None = None) -> str:
    """Get historic analyzed (backtest-like) dataframe for a pair.

    Args:
        pair: Trading pair (e.g. 'BTC/USDT').
        timeframe: Candle size (e.g. '5m', '1h').
        strategy: Strategy name to analyze with.
        timerange: Optional timerange (e.g. '20240101-').
        freqaimodel: Optional FreqAI model name.
    """
    return _safe_client_call("pair_history", pair, timeframe, strategy,
                             timerange, freqaimodel)


# ═══════════════════════════════════════════════════════════════════════
# 10. Configuration
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_config() -> str:
    """Get the current (sanitized) trading bot configuration."""
    return _safe_client_call("show_config")


@mcp.tool()
def reload_config() -> str:
    """Reload configuration from disk (applies changes without restart)."""
    return _safe_client_call("reload_config")


# ═══════════════════════════════════════════════════════════════════════
# 11. Custom Data
# ═══════════════════════════════════════════════════════════════════════


@mcp.tool()
def get_custom_data(trade_id: int, key: str | None = None) -> str:
    """Get custom data stored for a specific trade.

    Args:
        trade_id: The trade ID.
        key: Optional data key filter.
    """
    return _safe_client_call("list_custom_data", trade_id, key)


@mcp.tool()
def get_open_trades_custom_data(key: str | None = None,
                                limit: int = 100, offset: int = 0) -> str:
    """Get custom data across all currently open trades.

    Args:
        key: Optional data key filter.
        limit: Max results (default 100, max 500).
        offset: Pagination offset.
    """
    limit = min(limit, 500)
    return _safe_client_call("list_open_trades_custom_data", key, limit, offset)


# ═══════════════════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════════════════


def main():
    """Run the freqtrade-mcp-server via stdio transport.

    Usage:
        freqtrade-mcp-server

    Environment variables:
        FREQTRADE_URL      - API server URL (default: http://127.0.0.1:8080)
        FREQTRADE_USERNAME - API username   (default: freqtrade)
        FREQTRADE_PASSWORD - API password   (default: "")
    """
    mcp.run()


if __name__ == "__main__":
    main()
