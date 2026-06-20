# PyHound Installation

## Requirements

- **Python:** 3.8+
- **Optional:** Elasticsearch, Weaviate, Pinecone, or other vector DB for full diagnostics

## Install

### Via pip

```bash
pip install pyhound
```

### Via uv

```bash
uv add pyhound
```

### From Source

```bash
git clone https://github.com/Mullassery/pyhound.git
cd pyhound
pip install -e .
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

## Verify Installation

```python
import pyhound
print(pyhound.__version__)
```

## Optional Dependencies

### For Vector Database Support

```bash
# Elasticsearch
pip install pyhound[elasticsearch]

# Weaviate
pip install pyhound[weaviate]

# Pinecone
pip install pyhound[pinecone]
```

### For Full Development

```bash
pip install pyhound[dev]
```

## Docker

```bash
docker run -it mullassery/pyhound:latest
```

## Troubleshooting

For common installation issues, see [CONTRIBUTING.md](CONTRIBUTING.md#troubleshooting).
