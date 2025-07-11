import os
import time
from typing import Any
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

MAX_DRAW_DOWN = -500  # Hardcoded or pulled from config

def fetch_open_trades() -> list[dict[str, Any]]:
    """
    Fetches all open trades from the Supabase 'trades' table.
    """
    return supabase.table("trades") \
        .select("*") \
        .eq("status", "open") \
        .execute().data

def fetch_config() -> dict[str, Any]:
    """
    Fetches configuration settings from the Supabase 'config' table.
    """
    cfg = supabase.table("config").select("*").execute().data
    config_dict = {item['key']: item['value'] for item in cfg}
    return config_dict

def compute_drawdown() -> float:
    """
    Computes the current session drawdown using a Supabase RPC function.
    """
    result = supabase.rpc("calculate_drawdown").execute()
    return result.data if result.data else 0

def update_config_paused():
    """
    Updates the Supabase 'config' table to pause trading due to max drawdown.
    """
    supabase.table("config").upsert({
        "key": "trading_paused",
        "value": {"reason": "max_drawdown"}
    }).execute()

def update_trade_status(trade_id: int):
    """
    Updates the status of a specific trade to 'closed' in the Supabase 'trades' table.
    """
    supabase.table("trades") \
        .update({"status": "closed"}) \
        .eq("id", trade_id) \
        .execute()

def main():
    """
    Main function for the Risk Manager. Continuously monitors open trades
    and session drawdown, taking action if limits are breached.
    """
    print("🛡️ Risk Manager started...")

    while True:
        try:
            trades = fetch_open_trades()
            if not trades:
                print("✅ No open trades")
            else:
                for trade in trades:
                    # Simulated SL check
                    if trade["pnl"] is not None and trade["pnl"] < -100:
                        print(f"⚠️ SL breached on trade {trade['id']}")
                        update_trade_status(trade["id"])

            # Check session drawdown
            drawdown = compute_drawdown()
            print(f"📉 Session drawdown: {drawdown}")
            if drawdown <= MAX_DRAW_DOWN:
                update_config_paused()
                print("🚨 Trading paused due to drawdown limit")

        except Exception as e:
            print(f"[!] Risk Manager error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()