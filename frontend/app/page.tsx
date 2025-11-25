"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { api, RegimeInfo, ChaosMetrics } from "@/lib/api"
import { formatTitle } from "@/lib/i18n"

export default function Home() {
  const [regimeInfo, setRegimeInfo] = useState<RegimeInfo | null>(null)
  const [chaosMetrics, setChaosMetrics] = useState<ChaosMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        setError(null)
        const [regime, chaos] = await Promise.all([
          api.getRegimeInfo().catch(() => null),
          api.getChaosMetrics().catch(() => null),
        ])
        if (regime) setRegimeInfo(regime)
        if (chaos) setChaosMetrics(chaos)
        if (!regime && !chaos) {
          setError("无法连接到后端服务器。请确保后端在 http://localhost:8000 运行。")
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load data")
      } finally {
        setLoading(false)
      }
    }
    loadData()
    
    // Refresh data every 30 seconds
    const interval = setInterval(loadData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-muted-foreground">{formatTitle("加载中...", "Loading...")}</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">{formatTitle("错误", "Error")}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{error}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const regimeLabels: Record<string, string> = {
    TREND: formatTitle("趋势", "Trend"),
    NEUTRAL: formatTitle("中性", "Neutral"),
    CHAOTIC: formatTitle("混沌", "Chaotic"),
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">
          {formatTitle("SuperQuantLab 2.0", "SuperQuantLab 2.0")}
        </h1>
        <p className="text-muted-foreground">
          {formatTitle("加密货币量化研究与展示系统", "Crypto Quant Trading Engine & Research Platform")}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Regime Card */}
        {regimeInfo && (
          <Card>
            <CardHeader>
              <CardTitle>{formatTitle("当前市场状态", "Current Market Regime")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("状态", "Regime")}:</span>
                  <span className="font-semibold">{regimeLabels[regimeInfo.regime] || regimeInfo.regime}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("混沌指数", "Chaos Index")}:</span>
                  <span>{(regimeInfo.chaos_index * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("允许交易", "Allow Trading")}:</span>
                  <span>{regimeInfo.allow_new_trades ? "✓" : "✗"}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Chaos Metrics Card */}
        {chaosMetrics && (
          <Card>
            <CardHeader>
              <CardTitle>{formatTitle("混沌指标", "Chaos Metrics")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("混沌指数", "Chaos Index")}:</span>
                  <span>{(chaosMetrics.chaos_index * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("波动率", "Volatility")}:</span>
                  <span>{(chaosMetrics.volatility * 100).toFixed(2)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">{formatTitle("噪音信号比", "Noise/Signal")}:</span>
                  <span>{chaosMetrics.noise_to_signal_ratio.toFixed(2)}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Quick Actions Card */}
        <Card>
          <CardHeader>
            <CardTitle>{formatTitle("快速操作", "Quick Actions")}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm">
              <a href="/dashboard" className="block hover:text-primary transition-colors">
                → {formatTitle("查看策略表现", "View Performance")}
              </a>
              <a href="/strategies" className="block hover:text-primary transition-colors">
                → {formatTitle("管理策略", "Manage Strategies")}
              </a>
              <a href="/behavior" className="block hover:text-primary transition-colors">
                → {formatTitle("行为分析", "Behavior Analysis")}
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

