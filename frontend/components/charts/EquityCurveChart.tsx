"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { formatTitle } from "@/lib/i18n"

interface EquityPoint {
  timestamp: string
  equity: string | number
  drawdown: string | number
}

interface EquityCurveChartProps {
  data: EquityPoint[]
  title?: string
}

export function EquityCurveChart({ data, title }: EquityCurveChartProps) {
  // Transform data for chart
  const chartData = data.map((point) => ({
    time: new Date(point.timestamp).toLocaleDateString(),
    equity: typeof point.equity === "string" ? parseFloat(point.equity) : point.equity,
  }))

  const chartTitle = title || formatTitle("权益曲线", "Equity Curve")

  return (
    <Card>
      <CardHeader>
        <CardTitle>{chartTitle}</CardTitle>
        <CardDescription>{formatTitle("策略资金曲线变化", "Strategy equity curve over time")}</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="time"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="equity"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              name={formatTitle("权益", "Equity")}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

