/**
 * API Client for SuperQuantLab 2.0 Backend
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface BacktestRequest {
  strategy_configs: Array<{
    strategy_id: string;
    strategy_type: string;
    name: string;
    parameters: Record<string, any>;
  }>;
  symbol?: string;
  timeframe?: string;
  start_date?: string;
  end_date?: string;
  initial_capital?: number;
  fee_rate?: number;
  slippage_rate?: number;
}

export interface BacktestResponse {
  result: {
    strategy_id: string;
    strategy_name: string;
    start_date: string;
    end_date: string;
    initial_capital: string;
    final_capital: string;
    metrics: {
      total_return: string;
      annualized_return: string;
      sharpe_ratio: string;
      max_drawdown: string;
      win_rate: string;
      total_trades: number;
    };
    equity_curve: Array<{
      timestamp: string;
      equity: string;
      drawdown: string;
    }>;
    trades: any[];
  };
  success: boolean;
  message?: string;
}

export interface StrategyConfig {
  strategy_id: string;
  strategy_type: string;
  name: string;
  description?: string;
  parameters: Record<string, any>;
  enabled: boolean;
}

export interface ChaosMetrics {
  chaos_index: number;
  volatility: number;
  noise_to_signal_ratio: number;
  regime: string;
  timestamp: string;
}

export interface BehaviorMetrics {
  impulsiveness_index: number;
  chase_selloff_index: number;
  consecutive_losses: number;
  avg_operation_interval_ms: number;
  total_operations: number;
}

export interface RegimeInfo {
  regime: string;
  chaos_index: number;
  whale_activity_index: number;
  leverage_risk_index: number;
  position_multiplier: number;
  allow_new_trades: boolean;
  recommendations: Record<string, any>;
}

class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || `API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  // Backtest API
  async runBacktest(request: BacktestRequest): Promise<BacktestResponse> {
    return this.request<BacktestResponse>("/backtest/run", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  // Strategies API
  async listStrategies(): Promise<{ strategies: StrategyConfig[]; total: number }> {
    return this.request("/strategies");
  }

  async getStrategy(strategyId: string): Promise<StrategyConfig> {
    return this.request(`/strategies/${strategyId}`);
  }

  async createStrategy(config: Partial<StrategyConfig>): Promise<StrategyConfig> {
    return this.request("/strategies", {
      method: "POST",
      body: JSON.stringify(config),
    });
  }

  async generateStrategyFromLLM(
    description: string,
    language: string = "en"
  ): Promise<{ strategy: StrategyConfig; success: boolean; message?: string }> {
    return this.request("/strategies/from-llm", {
      method: "POST",
      body: JSON.stringify({ description, language }),
    });
  }

  async deleteStrategy(strategyId: string): Promise<{ success: boolean }> {
    return this.request(`/strategies/${strategyId}`, {
      method: "DELETE",
    });
  }

  // Metrics API
  async getChaosMetrics(
    symbol: string = "BTCUSDT",
    timeframe: string = "1h",
    window: number = 100
  ): Promise<ChaosMetrics> {
    return this.request(`/metrics/chaos?symbol=${symbol}&timeframe=${timeframe}&window=${window}`);
  }

  async getBehaviorMetrics(): Promise<BehaviorMetrics> {
    return this.request("/metrics/behavior");
  }

  async getRegimeInfo(
    symbol: string = "BTCUSDT",
    timeframe: string = "1h"
  ): Promise<RegimeInfo> {
    return this.request(`/metrics/regime?symbol=${symbol}&timeframe=${timeframe}`);
  }

  async getEquityCurve(strategyId?: string): Promise<any> {
    const url = strategyId
      ? `/metrics/equity?strategy_id=${strategyId}`
      : "/metrics/equity";
    return this.request(url);
  }
}

export const api = new APIClient();

