import { useTradingData } from './hooks/useTradingData';
import { PnLChart } from './components/PnLChart';

export default function DashboardPage() {
  const { pnlSeries, stats } = useTradingData();

  return (
    <div className="p-4 space-y-4">
      <div className="text-lg font-semibold">📊 Session Stats</div>
      <ul className="text-sm list-disc ml-4">
        <li>Total PnL: ₹{stats.total.toFixed(2)}</li>
        <li>Wins: {stats.win}</li>
        <li>Losses: {stats.loss}</li>
      </ul>

      <PnLChart data={pnlSeries} />
    </div>
  );
}