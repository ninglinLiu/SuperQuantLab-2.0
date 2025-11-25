"""
Backtest Engine: Core backtesting functionality with performance metrics
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict
import uuid

from app.models.market import (
    Candle,
    Bar,
    Signal,
    Trade,
    Order,
    Position,
    Portfolio,
    Side,
    OrderType,
    OrderStatus,
)
from app.models.strategy import (
    StrategyConfig,
    StrategyResult,
    PerformanceMetrics,
    EquityPoint,
)
from app.strategies.base import BaseStrategy
from app.strategies.ma_crossover import MACrossoverStrategy
from app.strategies.ma_cluster_density import MAClusterDensityStrategy


class BacktestEngine:
    """
    Backtesting engine that runs strategies on historical data.
    
    Supports:
    - Single and multi-strategy backtesting
    - Fees and slippage simulation
    - Performance metrics calculation
    - Equity curve generation
    """
    
    def __init__(
        self,
        initial_capital: Decimal = Decimal("100000"),
        fee_rate: Decimal = Decimal("0.001"),  # 0.1% fee
        slippage_rate: Decimal = Decimal("0.0005"),  # 0.05% slippage
    ):
        """
        Initialize backtest engine.
        
        Args:
            initial_capital: Starting capital
            fee_rate: Trading fee rate (e.g., 0.001 = 0.1%)
            slippage_rate: Slippage rate (e.g., 0.0005 = 0.05%)
        """
        self.initial_capital = initial_capital
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate
        
        self.portfolio: Optional[Portfolio] = None
        self.equity_curve: List[EquityPoint] = []
        self.trades: List[Trade] = []
        self.orders: List[Order] = []
    
    def _create_strategy(self, config: StrategyConfig) -> BaseStrategy:
        """Create strategy instance from config"""
        if config.strategy_type.value == "ma_crossover":
            return MACrossoverStrategy(config)
        elif config.strategy_type.value == "ma_cluster_density":
            return MAClusterDensityStrategy(config)
        else:
            raise ValueError(f"Unknown strategy type: {config.strategy_type}")
    
    def _apply_slippage(self, price: Decimal, side: Side) -> Decimal:
        """Apply slippage to price"""
        if side == Side.BUY:
            return price * (Decimal("1") + self.slippage_rate)
        else:
            return price * (Decimal("1") - self.slippage_rate)
    
    def _calculate_fee(self, quantity: Decimal, price: Decimal) -> Decimal:
        """Calculate trading fee"""
        return quantity * price * self.fee_rate
    
    def _execute_signal(
        self,
        signal: Signal,
        current_price: Decimal,
        portfolio: Portfolio,
    ) -> Optional[Trade]:
        """
        Execute a trading signal.
        
        Args:
            signal: Trading signal
            current_price: Current market price
            portfolio: Current portfolio state
        
        Returns:
            Trade object if executed, None otherwise
        """
        # Apply slippage
        execution_price = self._apply_slippage(current_price, signal.side)
        
        # Determine quantity
        if signal.quantity:
            # Use signal quantity (as percentage of equity)
            if signal.quantity <= Decimal("1"):  # Assume percentage
                quantity = portfolio.equity * signal.quantity / execution_price
            else:
                quantity = signal.quantity
        else:
            # Default position size (1% of equity)
            quantity = portfolio.equity * Decimal("0.01") / execution_price
        
        # Round quantity
        quantity = Decimal(str(round(float(quantity), 8)))
        
        if quantity <= 0:
            return None
        
        # Get or create position
        position = portfolio.positions.get(signal.symbol, Position(symbol=signal.symbol))
        
        # Calculate trade value
        trade_value = quantity * execution_price
        fee = self._calculate_fee(quantity, execution_price)
        
        # Check if we have enough cash for buy
        if signal.side == Side.BUY:
            if portfolio.cash < (trade_value + fee):
                # Not enough cash
                return None
            
            # Update position
            if position.quantity == 0:
                # New position
                position.quantity = quantity
                position.avg_price = execution_price
            else:
                # Add to existing long position
                total_value = position.quantity * position.avg_price + trade_value
                position.quantity += quantity
                position.avg_price = total_value / position.quantity
            
            # Update portfolio
            portfolio.cash -= (trade_value + fee)
        
        else:  # SELL
            # Check if we have position to sell
            if position.quantity <= 0:
                # No position to close
                return None
            
            # Close position (or partial close)
            close_quantity = min(quantity, position.quantity)
            
            # Calculate realized PnL
            realized_pnl = (execution_price - position.avg_price) * close_quantity - fee
            
            # Update position
            position.quantity -= close_quantity
            if position.quantity == 0:
                position.avg_price = Decimal("0")
            
            # Update portfolio
            portfolio.cash += (close_quantity * execution_price - fee)
            portfolio.realized_pnl += realized_pnl
        
        portfolio.positions[signal.symbol] = position
        
        # Create trade record
        trade = Trade(
            trade_id=str(uuid.uuid4()),
            timestamp=signal.timestamp,
            symbol=signal.symbol,
            side=signal.side,
            quantity=quantity,
            price=execution_price,
            fee=fee,
            strategy_id=signal.symbol,  # Use symbol as strategy ID for now
        )
        
        self.trades.append(trade)
        portfolio.trades.append(trade)
        
        return trade
    
    def _update_portfolio(self, portfolio: Portfolio, prices: Dict[str, Decimal]) -> None:
        """Update portfolio equity based on current prices"""
        portfolio.update_equity(prices)
    
    def _calculate_performance_metrics(
        self,
        equity_curve: List[EquityPoint],
        trades: List[Trade],
        initial_capital: Decimal,
        final_capital: Decimal,
    ) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics"""
        if not equity_curve:
            return PerformanceMetrics()
        
        # Total return
        total_return = (final_capital - initial_capital) / initial_capital
        
        # Annualized return (simplified: assume hourly bars, 24*365 hours/year)
        if len(equity_curve) > 1:
            start_date = equity_curve[0].timestamp
            end_date = equity_curve[-1].timestamp
            hours = (end_date - start_date).total_seconds() / 3600
            years = hours / (24 * 365)
            
            if years > 0:
                annualized_return = ((final_capital / initial_capital) ** (1 / years)) - Decimal("1")
            else:
                annualized_return = Decimal("0")
        else:
            annualized_return = Decimal("0")
        
        # Calculate returns for Sharpe ratio
        returns = []
        for i in range(1, len(equity_curve)):
            prev_equity = equity_curve[i-1].equity
            curr_equity = equity_curve[i].equity
            if prev_equity > 0:
                ret = (curr_equity - prev_equity) / prev_equity
                returns.append(float(ret))
        
        # Sharpe ratio (simplified)
        if returns:
            import numpy as np
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            if std_return > 0:
                # Annualize
                sharpe = Decimal(str(mean_return / std_return * np.sqrt(24 * 365)))
            else:
                sharpe = Decimal("0")
        else:
            sharpe = Decimal("0")
        
        # Max drawdown
        peak = initial_capital
        max_dd = Decimal("0")
        max_dd_duration = 0
        current_dd_duration = 0
        
        for point in equity_curve:
            if point.equity > peak:
                peak = point.equity
                current_dd_duration = 0
            else:
                dd = (peak - point.equity) / peak
                if dd > max_dd:
                    max_dd = dd
                current_dd_duration += 1
                if current_dd_duration > max_dd_duration:
                    max_dd_duration = current_dd_duration
        
        # Trade statistics
        winning_trades = [t for t in trades if self._is_winning_trade(t)]
        losing_trades = [t for t in trades if not self._is_winning_trade(t) and t.quantity > 0]
        
        win_rate = Decimal("0")
        if trades:
            win_rate = Decimal(str(len(winning_trades) / len(trades)))
        
        avg_win = Decimal("0")
        if winning_trades:
            wins = [self._trade_pnl(t) for t in winning_trades]
            avg_win = Decimal(str(sum(wins) / len(wins)))
        
        avg_loss = Decimal("0")
        if losing_trades:
            losses = [self._trade_pnl(t) for t in losing_trades]
            avg_loss = Decimal(str(sum(losses) / len(losses)))
        
        profit_factor = Decimal("0")
        if abs(avg_loss) > 0:
            total_wins = sum([self._trade_pnl(t) for t in winning_trades])
            total_losses = abs(sum([self._trade_pnl(t) for t in losing_trades]))
            if total_losses > 0:
                profit_factor = Decimal(str(total_wins / total_losses))
        
        # Avg R multiple (simplified)
        avg_r = Decimal("0")
        if avg_loss != 0:
            avg_r = avg_win / abs(avg_loss)
        
        return PerformanceMetrics(
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe,
            max_drawdown=max_dd,
            max_drawdown_duration=max_dd_duration,
            win_rate=win_rate,
            profit_factor=profit_factor,
            avg_r_multiple=avg_r,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            avg_win=avg_win,
            avg_loss=avg_loss,
        )
    
    def _is_winning_trade(self, trade: Trade) -> bool:
        """Check if trade is winning (simplified - compare with portfolio)"""
        # This is simplified - in real implementation, track entry/exit pairs
        return trade.side == Side.BUY  # Placeholder
    
    def _trade_pnl(self, trade: Trade) -> float:
        """Calculate trade PnL (simplified)"""
        # Simplified - real implementation needs entry/exit pairs
        return float(trade.net_value)
    
    def run(
        self,
        strategy_configs: List[StrategyConfig],
        candles: List[Candle],
    ) -> StrategyResult:
        """
        Run backtest on historical data.
        
        Args:
            strategy_configs: List of strategy configurations
            candles: Historical candle/bar data
        
        Returns:
            StrategyResult with backtest results
        """
        if not strategy_configs or not candles:
            raise ValueError("Strategy configs and candles are required")
        
        # Initialize
        self.portfolio = Portfolio(
            initial_capital=self.initial_capital,
            cash=self.initial_capital,
        )
        self.equity_curve = []
        self.trades = []
        
        # Create strategies (for now, use first strategy only)
        main_config = strategy_configs[0]
        strategy = self._create_strategy(main_config)
        strategy.reset()
        
        # Process each candle
        for candle in candles:
            bar = Bar.from_candle(candle)
            
            # Get signal from strategy
            signal = strategy.on_bar(bar)
            
            # Update current price
            current_prices = {candle.symbol: candle.close}
            
            # Execute signal if any
            if signal:
                self._execute_signal(signal, candle.close, self.portfolio)
            
            # Update portfolio equity
            self._update_portfolio(self.portfolio, current_prices)
            
            # Record equity point
            peak_equity = max([p.equity for p in self.equity_curve], default=self.initial_capital)
            drawdown = (peak_equity - self.portfolio.equity) / peak_equity if peak_equity > 0 else Decimal("0")
            
            self.equity_curve.append(
                EquityPoint(
                    timestamp=candle.timestamp,
                    equity=self.portfolio.equity,
                    drawdown=drawdown,
                )
            )
        
        # Finalize strategy
        strategy_result = strategy.on_finish()
        
        # Calculate metrics
        final_capital = self.portfolio.equity
        metrics = self._calculate_performance_metrics(
            self.equity_curve,
            self.trades,
            self.initial_capital,
            final_capital,
        )
        
        # Build result
        result = StrategyResult(
            strategy_id=main_config.strategy_id,
            strategy_name=main_config.name,
            start_date=candles[0].timestamp,
            end_date=candles[-1].timestamp,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            metrics=metrics,
            equity_curve=self.equity_curve,
            trades=self.trades,
        )
        
        return result

