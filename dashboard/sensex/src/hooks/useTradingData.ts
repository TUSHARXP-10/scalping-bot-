import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);

interface Trade {
  id: string;
  pnl: number;
  created_at: string;
  status: string;
  // Add other fields as needed based on your 'trades' table schema
}

export function useTradingData() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [pnlSeries, setPnlSeries] = useState<number[]>([]);
  const [stats, setStats] = useState({ total: 0, win: 0, loss: 0 });

  const fetchTrades = async () => {
    const { data } = await supabase
      .from('trades')
      .select('*')
      .order('created_at', { ascending: true });

    if (data) {
      setTrades(data);
      const pnl = data.map((t) => t.pnl || 0);
      setPnlSeries(pnl);

      const win = data.filter((t) => (t.pnl || 0) > 0).length;
      const loss = data.filter((t) => (t.pnl || 0) < 0).length;
      const total = pnl.reduce((a, b) => a + b, 0);
      setStats({ total, win, loss });
    }
  };

  useEffect(() => {
    fetchTrades();
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  return { trades, pnlSeries, stats };
}