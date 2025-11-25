"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { formatTitle } from "@/lib/i18n"

interface ChaosDataPoint {
  timestamp: string
  chaos_index: number
  regime?: string
}

interface ChaosIndexChartProps {
  data: ChaosDataPoint[]
  title?: string
}

export function ChaosIndexChart({ data, title }: ChaosIndexChartProps) {
  const chartData = data.map((point) => ({
    time: new Date(point.timestamp).toLocaleDateString(),
    chaosIndex: point.chaos_index * 100, // Convert to percentage
    regime: point.regime,
  }))

  const chartTitle = title || formatTitle("混沌指数", "Chaos Index")

  return (
    <Card>
      <CardHeader>
        <CardTitle>{chartTitle}</CardTitle>
        <CardDescription>{formatTitle("市场混沌度指标变化", "Market chaos index over time")}</CardDescription>
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
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
              formatter={(value: number) => [`${value.toFixed(2)}%`, formatTitle("混沌指数", "Chaos Index")]}
            />
            <ReferenceLine y={30} stroke="green" strokeDasharray="3 3" label="Trend" />
            <ReferenceLine y={70} stroke="red" strokeDasharray="3 3" label="Chaotic" />
            <Line
              type="monotone"
              dataKey="chaosIndex"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

