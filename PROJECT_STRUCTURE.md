# Project Structure

```
web-crawler-graph/
│
├── .github/
│   └── workflows/
│       └── python-ci.yml          # GitHub Actions CI/CD pipeline
│
├── crawler.py                     # Main crawler script
├── examples.py                    # Usage examples
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup configuration
│
├── README.md                      # Main documentation (EN/FA)
├── API.md                         # API reference
├── CONTRIBUTING.md                # Contribution guidelines (EN/FA)
├── CHANGELOG.md                   # Version history (EN/FA)
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
│
└── OUTPUT FILES (generated):
    ├── [domain]_interactive.html  # Interactive graph visualization
    ├── [domain]_links.json        # Detailed link data
    ├── [domain]_stats.json        # Basic statistics
    └── crawl_log.txt              # Execution log
```

## File Descriptions

### Core Files

#### `crawler.py`
Main application script containing three primary classes:
- `WebCrawler`: Handles web crawling logic
- `StatsGenerator`: Generates statistics and exports data
- `InteractiveGraphGenerator`: Creates interactive visualizations

**Key Features:**
- Multi-threaded crawling with ThreadPoolExecutor
- Rate limiting and retry logic
- URL normalization and validation
- NetworkX graph generation
- PyVis interactive visualization

#### `examples.py`
Demonstration scripts showing various usage patterns:
- Basic crawling
- Custom visualization settings
- Multiple site crawling

#### `requirements.txt`
Python package dependencies:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
networkx>=3.1
matplotlib>=3.7.0
tqdm>=4.66.0
pyvis>=0.3.2
lxml>=4.9.0
```

#### `setup.py`
Package configuration for PyPI distribution:
- Package metadata
- Dependencies
- Entry points for CLI

### Documentation Files

#### `README.md`
Comprehensive project documentation in English and Persian:
- Overview and features
- Installation instructions
- Usage examples
- Configuration options
- Troubleshooting
- FAQ

#### `API.md`
Complete API reference:
- Class documentation
- Method signatures
- Parameters and return types
- Code examples
- Data structures
- Error handling

#### `CONTRIBUTING.md`
Contribution guidelines in English and Persian:
- Bug reporting
- Feature requests
- Code contribution process
- Code style guidelines
- Testing requirements

#### `CHANGELOG.md`
Version history and release notes:
- New features
- Bug fixes
- Breaking changes
- Future plans

#### `LICENSE`
MIT License terms

### Configuration Files

#### `.gitignore`
Git ignore patterns:
- Python cache files
- Virtual environments
- IDE files
- Generated output files
- Log files

#### `.github/workflows/python-ci.yml`
GitHub Actions workflow:
- Automated testing
- Multiple Python version support
- Code linting
- Security checks

## Output Files

### Generated During Execution

#### `[domain]_interactive.html`
Interactive graph visualization file:
- Open in web browser
- Features search, zoom, pan
- Click to highlight connections
- Double-click to open URLs

**Technologies:**
- PyVis (vis.js)
- Custom JavaScript
- CSS styling

#### `[domain]_links.json`
Detailed link data in JSON format:
```json
[
  {
    "url": "https://example.com/page",
    "in_degree": 5,
    "out_degree": 10,
    "outgoing_links": ["https://example.com/other", ...]
  },
  ...
]
```

#### `[domain]_stats.json`
Basic statistics:
```json
{
  "nodes": 150,
  "edges": 450,
  "start_url": "https://example.com"
}
```

#### `crawl_log.txt`
Execution log with timestamps:
- Crawler initialization
- Progress updates
- Errors and warnings
- Completion status

## Code Organization

### Module Structure

```
crawler.py
│
├── Imports
│   ├── Standard library (requests, json, logging, etc.)
│   ├── Third-party (BeautifulSoup, networkx, pyvis)
│   └── Type hints (typing)
│
├── Configuration
│   └── Logging setup
│
├── Classes
│   ├── WebCrawler
│   │   ├── __init__()
│   │   ├── _extract_base_domain()
│   │   ├── _normalize_url()
│   │   ├── _is_internal_url()
│   │   ├── _fetch_page()
│   │   ├── _extract_links()
│   │   ├── _crawl_url()
│   │   └── crawl()
│   │
│   ├── StatsGenerator
│   │   ├── __init__()
│   │   ├── save_stats()
│   │   └── save_links()
│   │
│   └── InteractiveGraphGenerator
│       ├── __init__()
│       ├── get_node_info()
│       ├── generate()
│       └── _inject_js()
│
├── Utility Functions
│   └── get_safe_filename_base()
│
└── Main Execution
    └── main()
```

## Dependencies Graph

```
crawler.py
    ├── requests (HTTP requests)
    ├── beautifulsoup4 (HTML parsing)
    ├── networkx (Graph structure)
    ├── pyvis (Visualization)
    ├── tqdm (Progress bars)
    └── matplotlib (Optional, for static graphs)
```

## Data Flow

```
User Input (URL)
    ↓
WebCrawler.crawl()
    ↓
NetworkX Graph
    ↓
StatsGenerator
    ├→ stats.json
    └→ links.json
         ↓
    InteractiveGraphGenerator
         ↓
    interactive.html
```

## Installation Methods

### Method 1: Direct Use
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
pip install -r requirements.txt
python crawler.py https://example.com
```

### Method 2: Package Installation
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
pip install .
web-crawler https://example.com
```

### Method 3: Development Mode
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
pip install -e .
# Now you can edit the code and test immediately
```

## Testing

### Manual Testing
```bash
python crawler.py https://example.com
# Check generated files
ls -la *.html *.json
```

### Automated Testing (Future)
```bash
pytest tests/
```

## Deployment

### GitHub Release
1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to GitHub
5. Create release on GitHub

### PyPI Release (Future)
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Maintenance

### Regular Updates
- Update dependencies in `requirements.txt`
- Test with new Python versions
- Update documentation
- Address security vulnerabilities

### Version Scheme
Following Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH
- Example: 1.0.0

## Support Files

### Screenshots Directory (Optional)
```
screenshots/
├── graph_example.png
├── search_example.png
└── highlight_example.png
```

### Tests Directory (Future)
```
tests/
├── test_crawler.py
├── test_stats.py
└── test_visualizer.py
```

## Performance Considerations

### Memory Usage
- Small sites (<100 pages): ~50-100 MB
- Medium sites (100-1000 pages): ~100-500 MB
- Large sites (1000+ pages): ~500 MB - 2 GB

### Execution Time
- Depends on:
  - Number of pages
  - Rate limit setting
  - Max workers
  - Network speed
  - Server response time

### Optimization Tips
1. Adjust `max_workers` based on CPU cores
2. Increase `rate_limit` for respectful crawling
3. Monitor memory usage for large sites
4. Use SSD for better I/O performance

## Security Considerations

1. **robots.txt**: Currently not implemented
2. **Rate Limiting**: Prevents server overload
3. **User Agent**: Identifies the crawler
4. **HTTPS**: Supported by default
5. **Input Validation**: URL normalization

## Future Enhancements

Planned features (see CHANGELOG.md):
- robots.txt compliance
- Depth limit option
- Link validation
- Multiple export formats
- Database storage
- Web interface
- API endpoints
- Docker support
