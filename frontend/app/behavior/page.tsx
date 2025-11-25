"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { api, BehaviorMetrics } from "@/lib/api"
import { formatTitle } from "@/lib/i18n"

export default function BehaviorPage() {
  const [metrics, setMetrics] = useState<BehaviorMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadMetrics() {
      try {
        setLoading(true)
        const data = await api.getBehaviorMetrics()
        setMetrics(data)
      } catch (err) {
        console.error("Failed to load behavior metrics:", err)
      } finally {
        setLoading(false)
      }
    }
    loadMetrics()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-muted-foreground">{formatTitle("加载中...", "Loading...")}</p>
      </div>
    )
  }

  if (!metrics) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{formatTitle("错误", "Error")}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            {formatTitle("无法加载行为指标数据", "Failed to load behavior metrics")}
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">
          {formatTitle("行为金融分析", "Behavioral Finance Analysis")}
        </h1>
        <p className="text-muted-foreground">
          {formatTitle("交易行为模式与情绪分析", "Trading behavior patterns and sentiment analysis")}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Impulsiveness Index */}
        <Card>
          <CardHeader>
            <CardTitle>{formatTitle("冲动指数", "Impulsiveness Index")}</CardTitle>
            <CardDescription>
              {formatTitle("基于操作间隔的行为冲动度", "Behavior impulsiveness based on operation intervals")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold mb-2">
              {(metrics.impulsiveness_index * 100).toFixed(1)}%
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all"
                style={{ width: `${metrics.impulsiveness_index * 100}%` }}
              />
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              {metrics.impulsiveness_index > 0.7
                ? formatTitle("高冲动度 - 操作过于频繁", "High impulsiveness - operations too frequent")
                : metrics.impulsiveness_index > 0.4
                ? formatTitle("中等冲动度", "Moderate impulsiveness")
                : formatTitle("低冲动度 - 操作理性", "Low impulsiveness - rational operations")}
            </p>
          </CardContent>
        </Card>

        {/* Chase-Selloff Index */}
        <Card>
          <CardHeader>
            <CardTitle>{formatTitle("追涨杀跌指数", "Chase-Selloff Index")}</CardTitle>
            <CardDescription>
              {formatTitle("追高和恐慌性抛售行为统计", "Statistics on chasing highs and panic selling")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold mb-2">
              {(metrics.chase_selloff_index * 100).toFixed(1)}%
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-destructive h-2 rounded-full transition-all"
                style={{ width: `${metrics.chase_selloff_index * 100}%` }}
              />
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              {metrics.chase_selloff_index > 0.7
                ? formatTitle("高频追涨杀跌行为", "High frequency of chase-selloff behavior")
                : metrics.chase_selloff_index > 0.4
                ? formatTitle("中等追涨杀跌行为", "Moderate chase-selloff behavior")
                : formatTitle("理性交易行为", "Rational trading behavior")}
            </p>
          </CardContent>
        </Card>

        {/* Consecutive Losses */}
        <Card>
          <CardHeader>
            <CardTitle>{formatTitle("连续亏损", "Consecutive Losses")}</CardTitle>
            <CardDescription>
              {formatTitle("连续亏损交易次数", "Number of consecutive losing trades")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold mb-2">
              {metrics.consecutive_losses}
            </div>
            <p className="text-sm text-muted-foreground">
              {metrics.consecutive_losses >= 5
                ? formatTitle("⚠️ 连续亏损过多，建议暂停交易", "⚠️ Too many consecutive losses, recommend pausing trading")
                : metrics.consecutive_losses >= 3
                ? formatTitle("连续亏损较多，需谨慎", "Multiple consecutive losses, be cautious")
                : formatTitle("连续亏损在可接受范围", "Consecutive losses within acceptable range")}
            </p>
          </CardContent>
        </Card>

        {/* Operation Statistics */}
        <Card>
          <CardHeader>
            <CardTitle>{formatTitle("操作统计", "Operation Statistics")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">{formatTitle("总操作次数", "Total Operations")}:</span>
              <span className="font-semibold">{metrics.total_operations}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">
                {formatTitle("平均操作间隔", "Avg Operation Interval")}:
              </span>
              <span className="font-semibold">
                {metrics.avg_operation_interval_ms > 0
                  ? `${(metrics.avg_operation_interval_ms / 1000).toFixed(1)}s`
                  : "N/A"}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Trade Log Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>{formatTitle("交易日志", "Trade Log")}</CardTitle>
          <CardDescription>
            {formatTitle("最近的交易记录", "Recent trade records")}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            {formatTitle(
              "交易日志功能待实现（需要连接回测引擎）",
              "Trade log feature pending (requires backtest engine connection)"
            )}
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

