"""
Meta Strategy Engine: Meta-layer that adjusts strategy behavior based on market regime
"""
from decimal import Decimal
from typing import Dict, Optional
from datetime import datetime

from app.models.strategy import RegimeState, RegimeInfo
from app.engines.chaos_engine import ChaosEngine
from app.engines.microstructure_engine import MicrostructureEngine
from app.engines.behavior_engine import BehaviorEngine, BehaviorMetrics


class MetaEngine:
    """
    Meta Strategy Engine makes high-level decisions based on:
    - Chaos index
    - Whale activity
    - Leverage risk
    - Behavior metrics
    
    Outputs:
    - Position multiplier (0-1)
    - Allow new trades flag
    - Regime label
    """
    
    def __init__(self):
        """Initialize meta engine"""
        self.chaos_engine = ChaosEngine()
        self.microstructure_engine = MicrostructureEngine()
        self.behavior_engine = BehaviorEngine()
    
    def evaluate_regime(
        self,
        chaos_index: float,
        whale_activity_index: float,
        leverage_risk_index: float,
        behavior_metrics: Optional[BehaviorMetrics] = None,
    ) -> RegimeInfo:
        """
        Evaluate current market regime and generate meta decisions.
        
        Args:
            chaos_index: Chaos index (0-1)
            whale_activity_index: Whale activity index (0-1)
            leverage_risk_index: Leverage risk index (0-1)
            behavior_metrics: Behavior metrics (optional)
        
        Returns:
            RegimeInfo with decisions
        """
        # Classify regime
        regime = self.chaos_engine.classify_regime(chaos_index)
        
        # Calculate position multiplier
        # Start with base multiplier based on chaos
        if regime == RegimeState.TREND:
            base_multiplier = 1.0  # Full size in trends
        elif regime == RegimeState.CHAOTIC:
            base_multiplier = 0.3  # Reduce size in chaos
        else:  # NEUTRAL
            base_multiplier = 0.7  # Medium size
        
        # Adjust for leverage risk
        leverage_penalty = 1.0 - (leverage_risk_index * 0.3)  # Reduce by up to 30%
        position_multiplier = base_multiplier * leverage_penalty
        
        # Adjust for whale activity (high activity = be cautious)
        whale_penalty = 1.0 - (whale_activity_index * 0.2)  # Reduce by up to 20%
        position_multiplier *= whale_penalty
        
        # Adjust for behavior metrics (if available)
        if behavior_metrics:
            # High impulsiveness = reduce size
            impulsiveness_penalty = 1.0 - (behavior_metrics.impulsiveness_index * 0.2)
            position_multiplier *= impulsiveness_penalty
            
            # Consecutive losses = reduce size or halt
            if behavior_metrics.consecutive_losses >= 3:
                position_multiplier *= 0.5  # Halve position size
        
        # Clamp to [0, 1]
        position_multiplier = max(0.0, min(1.0, position_multiplier))
        
        # Decide if new trades are allowed
        allow_new_trades = True
        
        # Halt trading in extreme conditions
        if chaos_index > 0.9 and leverage_risk_index > 0.8:
            allow_new_trades = False
        elif regime == RegimeState.CHAOTIC and leverage_risk_index > 0.7:
            allow_new_trades = False
        elif behavior_metrics and behavior_metrics.consecutive_losses >= 5:
            allow_new_trades = False  # Stop after 5 consecutive losses
        
        return RegimeInfo(
            timestamp=datetime.now(),
            regime=regime,
            chaos_index=chaos_index,
            whale_activity_index=whale_activity_index,
            leverage_risk_index=leverage_risk_index,
            position_multiplier=float(position_multiplier),
            allow_new_trades=allow_new_trades,
        )
    
    def get_regime_recommendations(
        self,
        regime_info: RegimeInfo,
    ) -> Dict[str, any]:
        """
        Get human-readable recommendations based on regime.
        
        Args:
            regime_info: Current regime information
        
        Returns:
            Dict with recommendations
        """
        recommendations = {
            "regime": regime_info.regime.value,
            "position_size_pct": int(regime_info.position_multiplier * 100),
            "allow_trading": regime_info.allow_new_trades,
            "reason": "",
        }
        
        if regime_info.regime == RegimeState.TREND:
            recommendations["reason"] = "Trending market - normal position sizing"
        elif regime_info.regime == RegimeState.CHAOTIC:
            recommendations["reason"] = "Chaotic market - reduced position sizing"
            if not regime_info.allow_new_trades:
                recommendations["reason"] += " - trading halted"
        else:  # NEUTRAL
            recommendations["reason"] = "Neutral market - moderate position sizing"
        
        if regime_info.leverage_risk_index > 0.7:
            recommendations["reason"] += " - high leverage risk detected"
        
        if regime_info.whale_activity_index > 0.7:
            recommendations["reason"] += " - high whale activity"
        
        return recommendations

