# Data Directory

Place your historical OHLCV data files here.

## File Naming Convention

`{SYMBOL}_{TIMEFRAME}.csv`

Examples:
- `BTCUSDT_1h.csv`
- `ETHUSDT_4h.csv`
- `BTCUSDT_1d.csv`

## CSV Format

Required columns:
- `timestamp` (ISO format or Unix timestamp)
- `open` (float)
- `high` (float)
- `low` (float)
- `close` (float)
- `volume` (float)

Example:
```csv
timestamp,open,high,low,close,volume
2024-01-01T00:00:00,42000.0,42500.0,41800.0,42300.0,1234.56
2024-01-01T01:00:00,42300.0,42800.0,42200.0,42700.0,2345.67
```

## Data Sources

You can obtain historical data from:
- Binance API
- CoinGecko
- CryptoCompare
- Your own data provider

## TODO

- Add scripts to automatically download data from exchanges
- Support more data formats (JSON, Parquet, etc.)

