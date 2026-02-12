# Finance Big Data

1M transactions processing with Spark

## Setup

```bash
pip install -r requirements.txt
python generate_data.py
python spark/etl_pipeline.py
python dashboard/app.py
```

## Files

- `generate_data.py` - Create transaction data
- `spark/etl_pipeline.py` - Process with Spark
- `dashboard/app.py` - View results
- `realtime/live_feed.py` - Live data feed
