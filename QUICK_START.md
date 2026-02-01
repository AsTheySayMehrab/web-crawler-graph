# Quick Start Guide

Get started with Web Crawler & Graph Generator in 5 minutes!

## راهنمای سریع شروع (فارسی)

### نصب سریع

```bash
# 1. دانلود پروژه
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. اجرا
python crawler.py https://example.com
```

### نتیجه

سه فایل تولید می‌شود:
- `example_com_interactive.html` - گراف تعاملی
- `example_com_links.json` - داده‌های خام
- `example_com_stats.json` - آمار

### نمایش گراف

فایل HTML را در مرورگر باز کنید:
- جستجو: از کادر جستجو استفاده کنید
- هایلایت: روی نودها کلیک کنید
- باز کردن لینک: دابل‌کلیک روی نودها
- زوم: چرخ ماوس

---

## Quick Start (English)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git
cd web-crawler-graph

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python crawler.py https://example.com
```

### Output

Three files will be generated:
- `example_com_interactive.html` - Interactive graph
- `example_com_links.json` - Raw data
- `example_com_stats.json` - Statistics

### View Graph

Open the HTML file in a browser:
- Search: Use search box
- Highlight: Click on nodes
- Open link: Double-click on nodes
- Zoom: Mouse wheel

---

## Common Commands

### Crawl a website
```bash
python crawler.py https://yoursite.com
```

### Interactive mode
```bash
python crawler.py
# Enter URL when prompted
```

### Use examples
```bash
python examples.py
```

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x crawler.py
```

### Too slow?
Edit crawler.py:
```python
crawler = WebCrawler(url, max_workers=3, rate_limit=2.0)
```

---

## Next Steps

1. Read full documentation: `README.md`
2. Check API reference: `API.md`
3. See project structure: `PROJECT_STRUCTURE.md`
4. View examples: `examples.py`

---

## Support

- GitHub Issues: Report bugs or request features
- Documentation: Check README.md for details
- Examples: See examples.py for usage patterns

---

## Author

Mehrab Mahmoudifar
- GitHub: [@mehrabmahmoudifar](https://github.com/mehrabmahmoudifar)

---

## License

MIT License - Free to use and modify

---

## One-Line Installation

```bash
git clone https://github.com/mehrabmahmoudifar/web-crawler-graph.git && cd web-crawler-graph && pip install -r requirements.txt && python crawler.py
```
