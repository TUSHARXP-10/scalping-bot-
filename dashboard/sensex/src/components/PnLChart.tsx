import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

export function PnLChart({ data }: { data: number[] }) {
  const chartData = data.map((val, i) => ({ name: i + 1, pnl: val }));

  return (
    <div className="bg-white p-4 rounded-xl shadow w-full">
      <h2 className="text-xl font-bold mb-2">PnL Over Time</h2>
      <LineChart width={600} height={300} data={chartData}>
        <Line type="monotone" dataKey="pnl" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
}