import os
import time
from typing import Any
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SYMBOL = "SENSEX"
TICK_LIMIT = 50
SIGNAL_THRESHOLD = 0.6  # 60% probability confidence

def fetch_latest_ticks() -> pd.DataFrame:
    """
    Fetches the latest ticks for the specified symbol from Supabase.
    Returns a DataFrame of sorted ticks.
    """
    res = supabase.table("ticks") \
        .select("*") \
        .eq("symbol", SYMBOL) \
        .order("ts", desc=True) \
        .limit(TICK_LIMIT) \
        .execute()
    return pd.DataFrame(res.data).sort_values("ts")

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes technical indicators (EMA, RSI, VWAP, ATR) for the given DataFrame.
    """
    df['EMA_FAST'] = ta.ema(df['price'], length=5)
    df['EMA_SLOW'] = ta.ema(df['price'], length=14)
    df['RSI'] = ta.rsi(df['price'], length=14)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    return df

def apply_strategy(df: pd.DataFrame) -> dict[str, Any] | None:
    """
    Applies a trading strategy based on EMA crossovers.
    Returns a signal dictionary with type and strength, or None if no signal.
    """
    if len(df) < 15:
        return None

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    if prev['EMA_FAST'] < prev['EMA_SLOW'] and latest['EMA_FAST'] > latest['EMA_SLOW']:
        return {
            "type": "buy",
            "strength": round(0.7, 2)  # placeholder probability
        }
    elif prev['EMA_FAST'] > prev['EMA_SLOW'] and latest['EMA_FAST'] < latest['EMA_SLOW']:
        return {
            "type": "sell",
            "strength": round(0.7, 2)
        }

    return None

def insert_signal(signal_data: dict[str, Any]):
    """
    Inserts a new signal into the Supabase 'signals' table.
    """
    ticks = supabase.table("ticks") \
        .select("id") \
        .eq("symbol", SYMBOL) \
        .order("ts", desc=True) \
        .limit(1) \
        .execute()

    if ticks.data:
        latest_tick_id = ticks.data[0]['id']
        supabase.table("signals").insert({
            "tick_id": latest_tick_id,
            "type": signal_data["type"],
            "strength": signal_data["strength"]
        }).execute()
        print(f"[+] Inserted {signal_data['type']} signal with strength {signal_data['strength']}")

def main():
    """
    Main function to run the signal engine. Continuously fetches ticks,
    computes indicators, applies strategy, and inserts signals.
    """
    print("🧠 Starting Signal Engine...")
    while True:
        try:
            df = fetch_latest_ticks()

            if df.empty:
                print("⚠️ No ticks yet...")
                time.sleep(5)
                continue

            df['high'] = df['price'] * 1.01
            df['low'] = df['price'] * 0.99
            df['close'] = df['price']  # simulate OHLC

            df = compute_indicators(df)
            signal = apply_strategy(df)

            if signal:
                insert_signal(signal)
            else:
                print("❌ No signal generated")

        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()