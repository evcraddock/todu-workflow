# {name}

{description}

## Getting Started

### Prerequisites

- Python 3.11+
- pip or uv

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or with uv
uv pip install -r requirements.txt
```

### Development

```bash
python -m {name}
# or for web frameworks
uvicorn app.main:app --reload
```

## Testing

```bash
pytest
```

## License

MIT
