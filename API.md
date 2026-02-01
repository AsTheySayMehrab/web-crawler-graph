# API Documentation

Complete API reference for Web Crawler & Graph Generator.

## Classes

### WebCrawler

Main class for web crawling operations.

#### Constructor

```python
WebCrawler(start_url: str, max_workers: int = 5, rate_limit: float = 1.0)
```

**Parameters:**
- `start_url` (str): Starting URL for the crawl
- `max_workers` (int, optional): Number of concurrent threads. Default: 5
- `rate_limit` (float, optional): Minimum seconds between requests. Default: 1.0

**Example:**
```python
crawler = WebCrawler("https://example.com", max_workers=10, rate_limit=0.5)
```

#### Methods

##### crawl()

Execute the crawling process.

```python
def crawl() -> nx.DiGraph
```

**Returns:**
- `nx.DiGraph`: NetworkX directed graph representing website structure

**Example:**
```python
graph = crawler.crawl()
print(f"Found {graph.number_of_nodes()} pages")
```

##### _normalize_url()

Normalize and validate URLs.

```python
def _normalize_url(url: str, base_url: str = None) -> Optional[str]
```

**Parameters:**
- `url` (str): URL to normalize
- `base_url` (str, optional): Base URL for relative links

**Returns:**
- `str` or `None`: Normalized URL or None if invalid

##### _is_internal_url()

Check if URL belongs to same domain.

```python
def _is_internal_url(url: str) -> bool
```

**Parameters:**
- `url` (str): URL to check

**Returns:**
- `bool`: True if internal, False otherwise

##### _fetch_page()

Fetch page content with retry logic.

```python
def _fetch_page(url: str, retries: int = 3) -> Optional[str]
```

**Parameters:**
- `url` (str): URL to fetch
- `retries` (int, optional): Number of retry attempts. Default: 3

**Returns:**
- `str` or `None`: HTML content or None if failed

##### _extract_links()

Extract all links from HTML content.

```python
def _extract_links(html: str, base_url: str) -> List[str]
```

**Parameters:**
- `html` (str): HTML content
- `base_url` (str): Base URL for resolving relative links

**Returns:**
- `List[str]`: List of normalized URLs

---

### StatsGenerator

Generate statistics and export data.

#### Constructor

```python
StatsGenerator(graph: nx.DiGraph, start_url: str)
```

**Parameters:**
- `graph` (nx.DiGraph): NetworkX graph from crawler
- `start_url` (str): Starting URL of crawl

**Example:**
```python
stats_gen = StatsGenerator(graph, "https://example.com")
```

#### Methods

##### save_stats()

Save basic statistics to JSON.

```python
def save_stats(filename: str) -> Dict
```

**Parameters:**
- `filename` (str): Output filename

**Returns:**
- `Dict`: Statistics dictionary

**Example:**
```python
stats = stats_gen.save_stats("stats.json")
print(f"Total nodes: {stats['nodes']}")
```

##### save_links()

Save detailed link data to JSON.

```python
def save_links(filename: str) -> List[Dict]
```

**Parameters:**
- `filename` (str): Output filename

**Returns:**
- `List[Dict]`: List of link data dictionaries

**Example:**
```python
links = stats_gen.save_links("links.json")
print(f"Saved {len(links)} links")
```

---

### InteractiveGraphGenerator

Generate interactive visualizations.

#### Constructor

```python
InteractiveGraphGenerator(data_list: List[Dict])
```

**Parameters:**
- `data_list` (List[Dict]): Link data from StatsGenerator

**Example:**
```python
visualizer = InteractiveGraphGenerator(links_data)
```

#### Methods

##### generate()

Create interactive HTML graph.

```python
def generate(output_filename: str)
```

**Parameters:**
- `output_filename` (str): Output HTML filename

**Example:**
```python
visualizer.generate("graph.html")
```

##### get_node_info()

Extract display information from URL.

```python
def get_node_info(url: str) -> Tuple[str, str, str]
```

**Parameters:**
- `url` (str): URL to process

**Returns:**
- `Tuple[str, str, str]`: (label, group, decoded_url)

---

## Data Structures

### Stats Dictionary

```python
{
    "nodes": int,        # Total number of nodes
    "edges": int,        # Total number of edges
    "start_url": str     # Starting URL
}
```

### Link Data Dictionary

```python
{
    "url": str,              # Page URL
    "in_degree": int,        # Number of incoming links
    "out_degree": int,       # Number of outgoing links
    "outgoing_links": [str]  # List of outgoing URLs
}
```

---

## Graph Structure

### Node Attributes

- `label` (str): Display label
- `title` (str): Full URL (tooltip)
- `group` (str): Category (Mag, Business, Cloud, etc.)
- `color` (str): Hex color code
- `shape` (str): Node shape (default: "box")
- `font` (dict): Font settings

### Edge Attributes

- `color` (str): Edge color
- `arrows` (dict): Arrow settings
- `smooth` (dict): Curve settings

---

## Configuration

### Color Mapping

```python
color_map = {
    "Mag": "#E91E63",      # Pink
    "Business": "#4CAF50",  # Green
    "Cloud": "#2196F3",     # Blue
    "Shop": "#FF9800",      # Orange
    "Panel": "#9C27B0",     # Purple
    "Main": "#212121"       # Black
}
```

### Graph Options

```python
options = {
    "layout": {
        "hierarchical": {
            "enabled": True,
            "levelSeparation": 350,
            "nodeSpacing": 60,
            "direction": "LR"
        }
    },
    "physics": {"enabled": False},
    "interaction": {
        "hover": True,
        "navigationButtons": True
    }
}
```

---

## Error Handling

### Common Exceptions

- `requests.exceptions.RequestException`: Network errors
- `BeautifulSoup` parsing errors: Invalid HTML
- `ValueError`: Invalid URL format
- `KeyboardInterrupt`: User cancellation

### Example Error Handling

```python
try:
    crawler = WebCrawler("https://example.com")
    graph = crawler.crawl()
except KeyboardInterrupt:
    print("Crawl stopped by user")
except Exception as e:
    print(f"Error: {e}")
```

---

## Advanced Usage

### Custom Crawl Configuration

```python
# High-performance crawling
crawler = WebCrawler(
    start_url="https://example.com",
    max_workers=20,
    rate_limit=0.1
)

# Respectful crawling
crawler = WebCrawler(
    start_url="https://example.com",
    max_workers=2,
    rate_limit=2.0
)
```

### Programmatic Access

```python
from crawler import WebCrawler, StatsGenerator, InteractiveGraphGenerator

# Crawl
crawler = WebCrawler("https://example.com")
graph = crawler.crawl()

# Analyze
print(f"Nodes: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")

# Export
stats_gen = StatsGenerator(graph, "https://example.com")
links_data = stats_gen.save_links("output.json")

# Visualize
viz = InteractiveGraphGenerator(links_data)
viz.generate("graph.html")
```

---

## Command Line Interface

### Basic Usage

```bash
python crawler.py https://example.com
```

### Help

```bash
python crawler.py --help
```

### Arguments

- `url` (positional, optional): Starting URL
  - If not provided, will prompt interactively

---

## Logging

### Log Levels

- `INFO`: General information
- `ERROR`: Error messages
- `DEBUG`: Detailed debugging (not enabled by default)

### Log Output

Logs are written to:
- Console (stdout)
- `crawl_log.txt` file

### Example Log

```
2024-01-15 10:30:45 - INFO - Crawler initialized - Domain: example.com
2024-01-15 10:30:46 - INFO - Starting crawl from: https://example.com
2024-01-15 10:31:20 - INFO - Data saved to file: example_com_links.json
2024-01-15 10:31:25 - INFO - Interactive graph ready: example_com_interactive.html
```
