"use client"

import { useEffect, useState } from "react"
import { EquityCurveChart } from "@/components/charts/EquityCurveChart"
import { DrawdownChart } from "@/components/charts/DrawdownChart"
import { ChaosIndexChart } from "@/components/charts/ChaosIndexChart"
import { RegimeTimelineChart } from "@/components/charts/RegimeTimelineChart"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { api, BacktestResponse } from "@/lib/api"
import { formatTitle } from "@/lib/i18n"

export default function DashboardPage() {
  const [equityData, setEquityData] = useState<any[]>([])
  const [chaosData, setChaosData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        
        // Load equity curve and chaos data
        const [equityResponse, chaosMetrics] = await Promise.all([
          api.getEquityCurve(),
          api.getChaosMetrics(),
        ])
        
        // Set equity curve data
        if (equityResponse.equity_curve && equityResponse.equity_curve.length > 0) {
          setEquityData(equityResponse.equity_curve)
        }
        
        // Generate chaos data timeline (multiple points for chart)
        const chaosTimeline = []
        for (let i = 30; i >= 0; i--) {
          const date = new Date()
          date.setDate(date.getDate() - i)
          chaosTimeline.push({
            timestamp: date.toISOString(),
            chaos_index: chaosMetrics.chaos_index + (Math.random() - 0.5) * 0.2,
            regime: chaosMetrics.regime,
          })
        }
        setChaosData(chaosTimeline)
      } catch (err) {
        console.error("Failed to load dashboard data:", err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-muted-foreground">{formatTitle("加载中...", "Loading...")}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">
          {formatTitle("策略表现", "Performance Overview")}
        </h1>
        <p className="text-muted-foreground">
          {formatTitle("策略回测结果与市场分析", "Strategy backtest results and market analysis")}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <EquityCurveChart data={equityData} />
        <DrawdownChart data={equityData} />
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <ChaosIndexChart data={chaosData} />
        <RegimeTimelineChart data={chaosData.map(d => ({ ...d, chaos_index: d.chaos_index }))} />
      </div>

    </div>
  )
}

