"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { formatTitle } from "@/lib/i18n"

interface RegimePoint {
  timestamp: string
  regime: string
  chaos_index: number
}

interface RegimeTimelineChartProps {
  data: RegimePoint[]
  title?: string
}

export function RegimeTimelineChart({ data, title }: RegimeTimelineChartProps) {
  // Map regime to numeric value for chart
  const regimeMap: Record<string, number> = {
    TREND: 1,
    NEUTRAL: 2,
    CHAOTIC: 3,
  }

  const chartData = data.map((point) => ({
    time: new Date(point.timestamp).toLocaleDateString(),
    regime: regimeMap[point.regime] || 2,
    regimeLabel: point.regime,
    chaosIndex: point.chaos_index,
  }))

  const chartTitle = title || formatTitle("市场状态时间轴", "Regime Timeline")

  return (
    <Card>
      <CardHeader>
        <CardTitle>{chartTitle}</CardTitle>
        <CardDescription>{formatTitle("市场状态分类变化", "Market regime classification over time")}</CardDescription>
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
              domain={[0.5, 3.5]}
              tickFormatter={(value) => {
                const labels: Record<number, string> = {
                  1: formatTitle("趋势", "Trend"),
                  2: formatTitle("中性", "Neutral"),
                  3: formatTitle("混沌", "Chaotic"),
                }
                return labels[value] || ""
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
              formatter={(value: number, payload: any) => {
                const regimeLabels: Record<string, string> = {
                  TREND: formatTitle("趋势", "Trend"),
                  NEUTRAL: formatTitle("中性", "Neutral"),
                  CHAOTIC: formatTitle("混沌", "Chaotic"),
                }
                return [regimeLabels[payload.payload.regimeLabel] || payload.payload.regimeLabel, formatTitle("状态", "Regime")]
              }}
            />
            <Line
              type="stepAfter"
              dataKey="regime"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--primary))", r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

