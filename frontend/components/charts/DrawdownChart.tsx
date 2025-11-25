"use client"

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { formatTitle } from "@/lib/i18n"

interface DrawdownPoint {
  timestamp: string
  drawdown: string | number
}

interface DrawdownChartProps {
  data: DrawdownPoint[]
  title?: string
}

export function DrawdownChart({ data, title }: DrawdownChartProps) {
  const chartData = data.map((point) => ({
    time: new Date(point.timestamp).toLocaleDateString(),
    drawdown: typeof point.drawdown === "string" 
      ? parseFloat(point.drawdown) * 100 
      : point.drawdown * 100, // Convert to percentage
  }))

  const chartTitle = title || formatTitle("回撤", "Drawdown")

  return (
    <Card>
      <CardHeader>
        <CardTitle>{chartTitle}</CardTitle>
        <CardDescription>{formatTitle("策略回撤分析", "Strategy drawdown analysis")}</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="drawdownGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--destructive))" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="hsl(var(--destructive))" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="time"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
              tickFormatter={(value) => `${value.toFixed(1)}%`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
              formatter={(value: number) => [`${value.toFixed(2)}%`, formatTitle("回撤", "Drawdown")]}
            />
            <Area
              type="monotone"
              dataKey="drawdown"
              stroke="hsl(var(--destructive))"
              fillOpacity={1}
              fill="url(#drawdownGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

