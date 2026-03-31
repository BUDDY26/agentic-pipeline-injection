# structured_logger.py
# Shared logging module for all pipeline notebooks.
# Extracted from notebook_01_rag.ipynb Cell 2.
# Each run_id writes to its own experiment_logs/{run_id}.jsonl file.

import json
import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent / 'experiment_logs'
LOG_DIR.mkdir(exist_ok=True)


def log_entry(run_id: str, pipeline_type: str, agent_id: str,
              entry_type: str, content: str, extra: dict = None):
    """
    Append one JSON line to experiment_logs/{run_id}.jsonl.

    Args:
        run_id:        Unique run identifier (e.g. 'run_002').
        pipeline_type: Pipeline topology ('rag', 'linear', 'parallel').
        agent_id:      Agent name within the pipeline.
        entry_type:    'pre_generation' or 'post_generation'.
        content:       The assembled prompt or generated response string.
        extra:         Optional dict of additional fields to merge into the record.
    """
    record = {
        'run_id':        run_id,
        'pipeline_type': pipeline_type,
        'agent_id':      agent_id,
        'entry_type':    entry_type,
        'content':       content,
        'timestamp':     datetime.datetime.utcnow().isoformat() + 'Z',
    }
    if extra:
        record.update(extra)
    log_path = LOG_DIR / f'{run_id}.jsonl'
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')
    print(f'  [LOG] {entry_type} entry written to {log_path.name}')
