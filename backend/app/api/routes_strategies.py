"""
Strategies API routes
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.models.strategy import StrategyConfig, StrategyType
from app.services.llm_strategy_service import LLMStrategyService

router = APIRouter(prefix="/strategies", tags=["strategies"])

# In-memory storage (replace with database in production)
_strategies_db: dict[str, StrategyConfig] = {}

# Initialize with demo strategies
def _init_demo_strategies():
    """Initialize demo strategies"""
    from datetime import datetime
    demo_strategies = [
        StrategyConfig(
            strategy_id="demo_ma_crossover",
            strategy_type=StrategyType.MA_CROSSOVER,
            name="Demo MA Crossover",
            description="Moving average crossover strategy (10/30)",
            parameters={
                "short_window": 10,
                "long_window": 30,
                "position_size_pct": 0.1,
            },
            enabled=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        StrategyConfig(
            strategy_id="demo_ma_cluster",
            strategy_type=StrategyType.MA_CLUSTER_DENSITY,
            name="Demo MA Cluster Density",
            description="MA cluster density entry strategy",
            parameters={
                "ma_periods": [5, 10, 20, 30, 50],
                "density_threshold": 0.02,
                "breakout_multiplier": 1.5,
                "position_size_pct": 0.1,
            },
            enabled=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    for strategy in demo_strategies:
        _strategies_db[strategy.strategy_id] = strategy

# Initialize on module load
_init_demo_strategies()


class StrategyListResponse(BaseModel):
    """Strategy list response"""
    strategies: List[dict]
    total: int


class LLMStrategyRequest(BaseModel):
    """LLM strategy generation request"""
    description: str
    language: str = "en"


class LLMStrategyResponse(BaseModel):
    """LLM strategy generation response"""
    strategy: dict
    success: bool = True
    message: Optional[str] = None


@router.get("", response_model=StrategyListResponse)
async def list_strategies():
    """List all strategies"""
    strategies = [config.model_dump(mode="json") for config in _strategies_db.values()]
    return StrategyListResponse(
        strategies=strategies,
        total=len(strategies),
    )


@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str):
    """Get strategy by ID"""
    if strategy_id not in _strategies_db:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return _strategies_db[strategy_id].model_dump(mode="json")


@router.post("")
async def create_strategy(config: dict):
    """Create a new strategy"""
    strategy_config = StrategyConfig(**config)
    _strategies_db[strategy_config.strategy_id] = strategy_config
    return strategy_config.model_dump(mode="json")


@router.put("/{strategy_id}")
async def update_strategy(strategy_id: str, config: dict):
    """Update an existing strategy"""
    if strategy_id not in _strategies_db:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    strategy_config = StrategyConfig(**config)
    if strategy_config.strategy_id != strategy_id:
        raise HTTPException(status_code=400, detail="Strategy ID mismatch")
    
    _strategies_db[strategy_id] = strategy_config
    return strategy_config.model_dump(mode="json")


@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: str):
    """Delete a strategy"""
    if strategy_id not in _strategies_db:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    del _strategies_db[strategy_id]
    return {"success": True, "message": "Strategy deleted"}


@router.post("/from-llm", response_model=LLMStrategyResponse)
async def generate_strategy_from_llm(request: LLMStrategyRequest):
    """
    Generate strategy configuration from natural language description.
    
    Args:
        request: Natural language description and language code
    
    Returns:
        Generated StrategyConfig
    """
    try:
        service = LLMStrategyService()
        
        # Generate strategy (placeholder implementation)
        strategy_config = await service.generate_strategy_with_llm(
            description=request.description,
            language=request.language,
        )
        
        # Store in database
        _strategies_db[strategy_config.strategy_id] = strategy_config
        
        return LLMStrategyResponse(
            strategy=strategy_config.model_dump(mode="json"),
            success=True,
            message="Strategy generated successfully",
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Strategy generation failed: {str(e)}"
        )

