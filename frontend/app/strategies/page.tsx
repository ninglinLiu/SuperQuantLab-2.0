"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { api, StrategyConfig } from "@/lib/api"
import { formatTitle, texts } from "@/lib/i18n"

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<StrategyConfig[]>([])
  const [loading, setLoading] = useState(true)
  const [llmDescription, setLlmDescription] = useState("")
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    loadStrategies()
  }, [])

  async function loadStrategies() {
    try {
      setLoading(true)
      const response = await api.listStrategies()
      setStrategies(response.strategies)
    } catch (err) {
      console.error("Failed to load strategies:", err)
    } finally {
      setLoading(false)
    }
  }

  async function handleGenerateStrategy() {
    if (!llmDescription.trim()) {
      alert("Please enter a strategy description")
      return
    }

    try {
      setGenerating(true)
      const response = await api.generateStrategyFromLLM(llmDescription)
      if (response.success) {
        setLlmDescription("")
        await loadStrategies()
      }
    } catch (err) {
      console.error("Failed to generate strategy:", err)
      alert("Failed to generate strategy: " + (err instanceof Error ? err.message : "Unknown error"))
    } finally {
      setGenerating(false)
    }
  }

  async function handleDeleteStrategy(strategyId: string) {
    if (!confirm("Are you sure you want to delete this strategy?")) {
      return
    }

    try {
      await api.deleteStrategy(strategyId)
      await loadStrategies()
    } catch (err) {
      console.error("Failed to delete strategy:", err)
      alert("Failed to delete strategy")
    }
  }

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
          {formatTitle("策略管理", "Strategy Management")}
        </h1>
        <p className="text-muted-foreground">
          {formatTitle("创建、管理和生成量化策略", "Create, manage, and generate quant strategies")}
        </p>
      </div>

      {/* LLM Strategy Generator */}
      <Card>
        <CardHeader>
          <CardTitle>{formatTitle("使用LLM生成策略", "Generate Strategy with LLM")}</CardTitle>
          <CardDescription>
            {formatTitle(
              "输入自然语言描述，自动生成策略配置",
              "Enter a natural language description to generate strategy configuration"
            )}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <textarea
            className="w-full min-h-[100px] p-3 rounded-md border border-input bg-background text-foreground"
            placeholder="E.g., 'Moving average crossover strategy with 10 and 30 periods' or '均线交叉策略，短期10，长期30'"
            value={llmDescription}
            onChange={(e) => setLlmDescription(e.target.value)}
          />
          <Button
            onClick={handleGenerateStrategy}
            disabled={generating || !llmDescription.trim()}
          >
            {generating
              ? formatTitle("生成中...", "Generating...")
              : formatTitle("生成策略", "Generate Strategy")}
          </Button>
        </CardContent>
      </Card>

      {/* Strategies List */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">
          {formatTitle("已有策略", "Existing Strategies")} ({strategies.length})
        </h2>

        {strategies.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              {formatTitle("暂无策略。使用上方表单生成新策略。", "No strategies yet. Use the form above to generate a new strategy.")}
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {strategies.map((strategy) => (
              <Card key={strategy.strategy_id}>
                <CardHeader>
                  <CardTitle>{strategy.name}</CardTitle>
                  <CardDescription>
                    {strategy.description || `Type: ${strategy.strategy_type}`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">{formatTitle("策略ID", "Strategy ID")}:</span>
                      <span className="font-mono text-xs">{strategy.strategy_id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">{formatTitle("类型", "Type")}:</span>
                      <span>{strategy.strategy_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">{formatTitle("状态", "Status")}:</span>
                      <span>{strategy.enabled ? "✓ Enabled" : "✗ Disabled"}</span>
                    </div>
                  </div>
                  {Object.keys(strategy.parameters).length > 0 && (
                    <div className="mt-2 p-2 bg-muted rounded text-xs">
                      <div className="font-semibold mb-1">{formatTitle("参数", "Parameters")}:</div>
                      <pre className="whitespace-pre-wrap break-all">
                        {JSON.stringify(strategy.parameters, null, 2)}
                      </pre>
                    </div>
                  )}
                  <div className="flex gap-2 mt-4">
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDeleteStrategy(strategy.strategy_id)}
                    >
                      {formatTitle("删除", "Delete")}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

