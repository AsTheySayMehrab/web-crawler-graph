# Web Crawler & Interactive Graph Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful web crawler that maps website structure and generates interactive network visualizations.

[فارسی](#نسخه-فارسی) | [English](#english-version)

---

## English Version

### Overview

This tool crawls websites and creates beautiful interactive network graphs showing the relationship between pages. Perfect for:
- SEO analysis and internal linking structure
- Website architecture visualization
- Broken link detection
- Content hierarchy mapping

### Features

- **Smart Crawling**: Multi-threaded crawler with rate limiting and retry logic
- **Interactive Visualization**: PyVis-powered graphs with search, highlighting, and navigation
- **URL Normalization**: Handles relative URLs, query parameters, and redirects
- **Export Options**: JSON data export for further analysis
- **Domain-specific Grouping**: Automatic categorization by subdomain
- **Click to Navigate**: Double-click nodes to open URLs directly

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

```bash
python crawler.py https://example.com
```

#### Interactive Mode

```bash
python crawler.py
# You will be prompted to enter a URL
```

#### Command Line Arguments

```bash
python crawler.py [URL]
```

### Output Files

The tool generates three files:

1. **`[domain]_interactive.html`** - Interactive graph visualization (open in browser)
2. **`[domain]_links.json`** - Detailed link data with in/out degrees
3. **`[domain]_stats.json`** - Basic statistics (nodes, edges, start URL)

### Interactive Graph Features

- **Search**: Find nodes by URL or label
- **Highlight**: Click nodes to highlight connections
  - Red edges: Outgoing links
  - Blue edges: Incoming links
- **Navigate**: Double-click nodes to open URLs in new tab
- **Reset**: Return to original view
- **Zoom & Pan**: Mouse wheel and drag to navigate

### Configuration

Modify crawler behavior in `WebCrawler.__init__()`:

- `max_workers`: Number of concurrent threads (default: 5)
- `rate_limit`: Minimum seconds between requests (default: 1.0)

### Technical Details

#### Architecture

```
WebCrawler → StatsGenerator → InteractiveGraphGenerator
     ↓              ↓                    ↓
  NetworkX       JSON Files         HTML Visualization
```

#### Node Grouping

Nodes are automatically categorized by subdomain:

| Subdomain | Group | Color |
|-----------|-------|-------|
| mag.* | Mag | Pink (#E91E63) |
| business.* | Business | Green (#4CAF50) |
| cloud.* | Cloud | Blue (#2196F3) |
| shop.* | Shop | Orange (#FF9800) |
| my.* | Panel | Purple (#9C27B0) |
| (root) | Main | Black (#212121) |

### Examples

#### Example 1: Crawl a blog
```bash
python crawler.py https://myblog.com
```

Output:
- `myblog_com_interactive.html`
- `myblog_com_links.json`
- `myblog_com_stats.json`

#### Example 2: Analyze e-commerce site
```bash
python crawler.py https://shop.example.com
```

### Requirements

- Python 3.8+
- Internet connection
- Modern web browser (for viewing graphs)

### Dependencies

See `requirements.txt` for full list:
- requests - HTTP library
- beautifulsoup4 - HTML parsing
- networkx - Graph data structure
- pyvis - Interactive visualization
- tqdm - Progress bars

### Troubleshooting

**Issue: Too slow**
- Reduce `max_workers`
- Increase `rate_limit`

**Issue: Memory error**
- Large sites may require more RAM
- Consider crawling specific sections

**Issue: Access denied**
- Website may block crawlers
- Check `robots.txt`

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

### License

MIT License - see LICENSE file for details

### Author

**Mehrab Mahmoudifar**
- GitHub: [@AsTheySayMehrab](https://github.com/AsTheySayMehrab)

### Acknowledgments

Built with:
- NetworkX for graph processing
- PyVis for visualization
- BeautifulSoup for HTML parsing

---

## نسخه فارسی

### معرفی

این ابزار وب‌سایت‌ها را خزیده و نمودارهای شبکه‌ای تعاملی زیبایی از ساختار صفحات ایجاد می‌کند.

### ویژگی‌ها

- **خزش هوشمند**: کراولر چند-نخی با محدودیت سرعت و منطق تکرار
- **نمایش تعاملی**: گراف‌های PyVis با جستجو، هایلایت و ناوبری
- **نرمال‌سازی URL**: مدیریت URLهای نسبی، پارامترهای کوئری و ریدایرکت‌ها
- **گزینه‌های خروجی**: خروجی JSON برای تحلیل بیشتر
- **گروه‌بندی دامنه‌ای**: دسته‌بندی خودکار بر اساس ساب‌دامین
- **کلیک برای باز کردن**: دابل‌کلیک روی نودها برای باز کردن URL

### نصب

1. کلون کردن مخزن:
```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

### استفاده

#### استفاده ساده

```bash
python crawler.py https://example.com
```

#### حالت تعاملی

```bash
python crawler.py
# از شما خواسته می‌شود URL وارد کنید
```

### فایل‌های خروجی

این ابزار سه فایل تولید می‌کند:

1. **`[domain]_interactive.html`** - نمایش گراف تعاملی (در مرورگر باز کنید)
2. **`[domain]_links.json`** - داده‌های دقیق لینک‌ها با درجات ورودی/خروجی
3. **`[domain]_stats.json`** - آمار پایه (نودها، یال‌ها، URL شروع)

### ویژگی‌های گراف تعاملی

- **جستجو**: یافتن نودها با URL یا برچسب
- **هایلایت**: کلیک روی نودها برای هایلایت ارتباطات
  - یال‌های قرمز: لینک‌های خروجی
  - یال‌های آبی: لینک‌های ورودی
- **ناوبری**: دابل‌کلیک روی نودها برای باز کردن URL در تب جدید
- **ریست**: بازگشت به نمای اصلی
- **زوم و پن**: چرخ ماوس و کشیدن برای حرکت

### پیکربندی

تغییر رفتار کراولر در `WebCrawler.__init__()`:

- `max_workers`: تعداد نخ‌های همزمان (پیش‌فرض: 5)
- `rate_limit`: حداقل ثانیه بین درخواست‌ها (پیش‌فرض: 1.0)

### جزئیات فنی

#### معماری

```
WebCrawler → StatsGenerator → InteractiveGraphGenerator
     ↓              ↓                    ↓
  NetworkX       JSON Files         HTML Visualization
```

#### گروه‌بندی نودها

نودها به صورت خودکار بر اساس ساب‌دامین دسته‌بندی می‌شوند:

| ساب‌دامین | گروه | رنگ |
|-----------|-------|-------|
| mag.* | Mag | صورتی (#E91E63) |
| business.* | Business | سبز (#4CAF50) |
| cloud.* | Cloud | آبی (#2196F3) |
| shop.* | Shop | نارنجی (#FF9800) |
| my.* | Panel | بنفش (#9C27B0) |
| (ریشه) | Main | سیاه (#212121) |

### مثال‌ها

#### مثال 1: خزش یک وبلاگ
```bash
python crawler.py https://myblog.com
```

خروجی:
- `myblog_com_interactive.html`
- `myblog_com_links.json`
- `myblog_com_stats.json`

#### مثال 2: تحلیل سایت فروشگاهی
```bash
python crawler.py https://shop.example.com
```

### نیازمندی‌ها

- Python 3.8 یا بالاتر
- اتصال به اینترنت
- مرورگر وب مدرن (برای نمایش گراف‌ها)

### وابستگی‌ها

لیست کامل در `requirements.txt`:
- requests - کتابخانه HTTP
- beautifulsoup4 - تجزیه HTML
- networkx - ساختار داده گراف
- pyvis - نمایش تعاملی
- tqdm - نوار پیشرفت

### عیب‌یابی

**مشکل: خیلی کند است**
- `max_workers` را کاهش دهید
- `rate_limit` را افزایش دهید

**مشکل: خطای حافظه**
- سایت‌های بزرگ ممکن است RAM بیشتری نیاز داشته باشند
- خزش بخش‌های خاص را در نظر بگیرید

**مشکل: دسترسی رد شد**
- وب‌سایت ممکن است کراولرها را مسدود کند
- `robots.txt` را بررسی کنید

### مشارکت

مشارکت‌ها خوش‌آمدید! لطفاً:
1. مخزن را Fork کنید
2. یک شاخه ویژگی ایجاد کنید
3. Pull Request ارسال کنید

### مجوز

مجوز MIT - جزئیات در فایل LICENSE

### نویسنده

**محراب محمودی‌فر**
- GitHub: [@AsTheySayMehrab](https://github.com/AsTheySayMehrab)

### قدردانی

ساخته شده با:
- NetworkX برای پردازش گراف
- PyVis برای نمایش‌سازی
- BeautifulSoup برای تجزیه HTML

---

## Screenshots / تصاویر

### Interactive Graph / گراف تعاملی
![Graph Example](screenshots/graph_example.png)

### Search Feature / ویژگی جستجو
![Search Feature](screenshots/search_example.png)

### Highlight Connections / هایلایت ارتباطات
![Highlight](screenshots/highlight_example.png)

---

## Roadmap / نقشه راه

- [ ] Add depth limit option
- [ ] Export to other formats (GEXF, GraphML)
- [ ] Parallel domain crawling
- [ ] Custom color schemes
- [ ] Link validation (check for 404s)
- [ ] Content analysis features

---

## FAQ

**Q: Can I crawl external domains?**
A: No, the crawler only follows internal links to prevent scope creep.

**Q: How do I handle large websites?**
A: Consider increasing rate_limit and decreasing max_workers to be respectful of server resources.

**Q: Does it respect robots.txt?**
A: Currently no, but this is planned for future versions. Please use responsibly.

---

**Star this repo if you find it useful!** ⭐
