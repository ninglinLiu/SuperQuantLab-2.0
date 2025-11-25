/**
 * Simple bilingual text management for SuperQuantLab 2.0
 */
export const texts = {
  dashboard: {
    title: { zh: "策略表现", en: "Performance Overview" },
    equityCurve: { zh: "权益曲线", en: "Equity Curve" },
    drawdown: { zh: "回撤", en: "Drawdown" },
    chaosIndex: { zh: "混沌指数", en: "Chaos Index" },
    regimeTimeline: { zh: "市场状态时间轴", en: "Regime Timeline" },
    behaviorStatus: { zh: "行为状态", en: "Behavior Status" },
    microstructureStatus: { zh: "微结构状态", en: "Microstructure Status" },
  },
  strategies: {
    title: { zh: "策略管理", en: "Strategy Management" },
    create: { zh: "创建策略", en: "Create Strategy" },
    generateWithLLM: { zh: "使用LLM生成策略", en: "Generate Strategy with LLM" },
    description: { zh: "描述", en: "Description" },
    generate: { zh: "生成", en: "Generate" },
    delete: { zh: "删除", en: "Delete" },
    edit: { zh: "编辑", en: "Edit" },
  },
  behavior: {
    title: { zh: "行为金融分析", en: "Behavioral Finance Analysis" },
    impulsiveness: { zh: "冲动指数", en: "Impulsiveness Index" },
    chaseSelloff: { zh: "追涨杀跌指数", en: "Chase-Selloff Index" },
    consecutiveLosses: { zh: "连续亏损", en: "Consecutive Losses" },
    tradeLog: { zh: "交易日志", en: "Trade Log" },
  },
  common: {
    loading: { zh: "加载中...", en: "Loading..." },
    error: { zh: "错误", en: "Error" },
    success: { zh: "成功", en: "Success" },
    cancel: { zh: "取消", en: "Cancel" },
    confirm: { zh: "确认", en: "Confirm" },
  },
} as const;

/**
 * Get bilingual text (shows both languages)
 */
export function getText(key: keyof typeof texts, subKey?: string): string {
  // For now, return both languages
  if (subKey && key in texts) {
    const section = texts[key as keyof typeof texts] as any;
    if (subKey in section) {
      const item = section[subKey];
      return `${item.zh} ${item.en}`;
    }
  }
  return "";
}

/**
 * Format bilingual title
 */
export function formatTitle(zh: string, en: string): string {
  return `${zh} ${en}`;
}

