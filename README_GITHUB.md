<div align="center">

# Web Crawler & Interactive Graph Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mehrabmahmoudifar/web-crawler-graph?style=social)](https://github.com/mehrabmahmoudifar/web-crawler-graph/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/mehrabmahmoudifar/web-crawler-graph?style=social)](https://github.com/mehrabmahmoudifar/web-crawler-graph/network/members)

**A powerful web crawler that maps website structure and generates beautiful interactive network visualizations.**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

<img src="screenshots/demo.gif" alt="Demo" width="800">

[🇬🇧 English](#english) | [🇮🇷 فارسی](#persian)

</div>

---

## English

### Features

- 🚀 **Multi-threaded Crawling** - Fast concurrent crawling with configurable workers
- 🎨 **Interactive Visualization** - Beautiful PyVis graphs with search and highlighting
- 🔍 **Smart URL Handling** - Automatic normalization, deduplication, and validation
- 📊 **Data Export** - JSON export for further analysis
- 🎯 **Domain Grouping** - Automatic categorization by subdomain
- 🖱️ **Interactive Navigation** - Click to highlight, double-click to open URLs
- ⚡ **Rate Limiting** - Respectful crawling with configurable delays
- 📝 **Comprehensive Logging** - Detailed execution logs

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph

# Install dependencies
pip install -r requirements.txt

# Run the crawler
python crawler.py https://example.com
```

### Output Files

| File | Description |
|------|-------------|
| `[domain]_interactive.html` | 🎨 Interactive graph visualization |
| `[domain]_links.json` | 📊 Detailed link data |
| `[domain]_stats.json` | 📈 Basic statistics |
| `crawl_log.txt` | 📝 Execution log |

### Interactive Graph Features

<table>
<tr>
<td width="50%">

**Search & Navigation**
- Find nodes by URL or label
- Zoom and pan controls
- Navigation buttons
- Keyboard shortcuts

</td>
<td width="50%">

**Visual Features**
- Color-coded by subdomain
- Hierarchical layout
- Smooth curved edges
- Hover tooltips

</td>
</tr>
<tr>
<td width="50%">

**Interactions**
- Click to highlight connections
- Double-click to open URLs
- Right-click for context menu
- Reset view button

</td>
<td width="50%">

**Data Display**
- In-degree indicators
- Out-degree indicators
- Connection highlighting
- Node grouping

</td>
</tr>
</table>

### Installation Options

#### Option 1: Basic Installation
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
pip install -r requirements.txt
```

#### Option 2: Package Installation
```bash
pip install git+https://github.com/mehrabmahmoudifar/web-crawler-graph.git
```

#### Option 3: Development Mode
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
pip install -e .
```

### Usage Examples

#### Basic Crawl
```python
from crawler import WebCrawler

crawler = WebCrawler("https://example.com")
graph = crawler.crawl()
print(f"Found {graph.number_of_nodes()} pages")
```

#### Custom Configuration
```python
from crawler import WebCrawler, StatsGenerator, InteractiveGraphGenerator

# High-performance crawling
crawler = WebCrawler(
    start_url="https://example.com",
    max_workers=10,
    rate_limit=0.5
)

graph = crawler.crawl()

# Generate visualization
stats_gen = StatsGenerator(graph, "https://example.com")
links_data = stats_gen.save_links("links.json")

visualizer = InteractiveGraphGenerator(links_data)
visualizer.generate("graph.html")
```

#### Command Line
```bash
# Basic usage
python crawler.py https://example.com

# Interactive mode
python crawler.py
```

### Requirements

- Python 3.8 or higher
- Internet connection
- Modern web browser (for viewing graphs)

### Dependencies

```
requests>=2.31.0
beautifulsoup4>=4.12.0
networkx>=3.1
matplotlib>=3.7.0
tqdm>=4.66.0
pyvis>=0.3.2
lxml>=4.9.0
```

### Documentation

- 📖 [Full Documentation](README.md)
- 🔧 [API Reference](API.md)
- 🏗️ [Project Structure](PROJECT_STRUCTURE.md)
- 🚀 [Quick Start Guide](QUICK_START.md)
- 📝 [Changelog](CHANGELOG.md)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)

### Screenshots

<details>
<summary>Click to view screenshots</summary>

#### Interactive Graph
![Graph Example](screenshots/graph_example.png)

#### Search Feature
![Search Feature](screenshots/search_example.png)

#### Highlight Connections
![Highlight](screenshots/highlight_example.png)

</details>

### Performance

| Website Size | Nodes | Time | Memory |
|--------------|-------|------|---------|
| Small (<100 pages) | 50-100 | 1-2 min | 50-100 MB |
| Medium (100-1000 pages) | 100-500 | 5-15 min | 100-500 MB |
| Large (1000+ pages) | 500+ | 15+ min | 500 MB - 2 GB |

### Configuration

Modify crawler behavior:

```python
WebCrawler(
    start_url="https://example.com",
    max_workers=5,      # Number of concurrent threads
    rate_limit=1.0      # Minimum seconds between requests
)
```

### Node Color Groups

| Subdomain | Group | Color |
|-----------|-------|-------|
| mag.* | Mag | 🟣 Pink (#E91E63) |
| business.* | Business | 🟢 Green (#4CAF50) |
| cloud.* | Cloud | 🔵 Blue (#2196F3) |
| shop.* | Shop | 🟠 Orange (#FF9800) |
| my.* | Panel | 🟣 Purple (#9C27B0) |
| (root) | Main | ⚫ Black (#212121) |

### Troubleshooting

<details>
<summary>Common Issues & Solutions</summary>

#### Issue: Too slow
**Solution:** Reduce `max_workers` or increase `rate_limit`
```python
crawler = WebCrawler(url, max_workers=3, rate_limit=2.0)
```

#### Issue: Memory error
**Solution:** Crawl specific sections or use more RAM

#### Issue: Access denied
**Solution:** Check website's `robots.txt` and respect their policies

#### Issue: ModuleNotFoundError
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

</details>

### Roadmap

- [ ] robots.txt compliance
- [ ] Depth limit configuration
- [ ] Link validation (404 detection)
- [ ] Export to GEXF/GraphML
- [ ] Custom color schemes
- [ ] Content analysis
- [ ] Parallel domain crawling
- [ ] Web interface
- [ ] Docker support
- [ ] API endpoints

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Author

**Mehrab Mahmoudifar**

- GitHub: [@mehrabmahmoudifar](https://github.com/mehrabmahmoudifar)
- Email: mehrab.mahmoudifar@example.com

### Acknowledgments

Built with:
- [NetworkX](https://networkx.org/) - Graph processing
- [PyVis](https://pyvis.readthedocs.io/) - Interactive visualization
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Requests](https://requests.readthedocs.io/) - HTTP library

### Support

If you find this project helpful, please give it a ⭐ on GitHub!

<div align="center">

**[⬆ Back to top](#web-crawler--interactive-graph-generator)**

</div>

---

## Persian

<div dir="rtl" align="right">

### ویژگی‌ها

- 🚀 **خزش چند-نخی** - خزش سریع همزمان با کارگرهای قابل تنظیم
- 🎨 **نمایش تعاملی** - گراف‌های زیبای PyVis با جستجو و هایلایت
- 🔍 **مدیریت هوشمند URL** - نرمال‌سازی، حذف تکراری و اعتبارسنجی خودکار
- 📊 **خروجی داده** - خروجی JSON برای تحلیل بیشتر
- 🎯 **گروه‌بندی دامنه** - دسته‌بندی خودکار بر اساس ساب‌دامین
- 🖱️ **ناوبری تعاملی** - کلیک برای هایلایت، دابل‌کلیک برای باز کردن URL
- ⚡ **محدودیت سرعت** - خزش محترمانه با تأخیرهای قابل تنظیم
- 📝 **لاگ جامع** - لاگ‌های دقیق اجرا

### شروع سریع

```bash
# کلون کردن مخزن
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای کراولر
python crawler.py https://example.com
```

### فایل‌های خروجی

| فایل | توضیحات |
|------|-------------|
| `[domain]_interactive.html` | 🎨 نمایش گراف تعاملی |
| `[domain]_links.json` | 📊 داده‌های دقیق لینک |
| `[domain]_stats.json` | 📈 آمار پایه |
| `crawl_log.txt` | 📝 لاگ اجرا |

### مستندات

- 📖 [مستندات کامل](README.md)
- 🔧 [مرجع API](API.md)
- 🏗️ [ساختار پروژه](PROJECT_STRUCTURE.md)
- 🚀 [راهنمای شروع سریع](QUICK_START.md)
- 📝 [تغییرات](CHANGELOG.md)
- 🤝 [راهنمای مشارکت](CONTRIBUTING.md)

### نیازمندی‌ها

- Python 3.8 یا بالاتر
- اتصال به اینترنت
- مرورگر وب مدرن (برای نمایش گراف‌ها)

### نویسنده

**محراب محمودی‌فر**

- GitHub: [@astheysaymehrab](https://github.com/astheysaymehrab)
- ایمیل: mehrabmahmoudifar98@gmail.com

### مجوز

این پروژه تحت مجوز MIT منتشر شده است - فایل [LICENSE](LICENSE) را برای جزئیات ببینید.

### پشتیبانی

اگر این پروژه برای شما مفید بود، لطفاً در GitHub یک ⭐ بدهید!

</div>

<div align="center">

**Made with ❤️ by Mehrab Mahmoudifar**

</div>
