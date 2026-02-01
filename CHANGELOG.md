# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- Initial release of Web Crawler & Graph Generator
- Multi-threaded web crawler with rate limiting
- Interactive PyVis graph visualization
- URL normalization and validation
- JSON export functionality
- Search and highlight features in interactive graph
- Double-click to open URLs
- Subdomain-based node grouping
- Hierarchical graph layout
- Command-line interface
- Progress bars with tqdm
- Comprehensive logging system
- Bilingual README (English/Persian)

### Features
- Concurrent crawling with configurable workers
- Retry logic with exponential backoff
- Automatic duplicate URL detection
- Internal link filtering
- Graph statistics generation
- Interactive node search
- Connection highlighting
- Customizable color schemes by subdomain
- Responsive HTML output

### Technical
- Python 3.8+ support
- NetworkX for graph operations
- BeautifulSoup4 for HTML parsing
- PyVis for interactive visualization
- Requests for HTTP operations
- Type hints throughout codebase

## [Unreleased]

### Planned
- robots.txt respect
- Depth limit configuration
- Link validation (404 detection)
- Export to GEXF/GraphML formats
- Custom color scheme support
- Content analysis features
- Parallel domain crawling
- API endpoint support
- Database storage options
- Web interface

---

## نسخه‌ها

## [1.0.0] - 1403/10/25

### اضافه شده
- انتشار اولیه کراولر وب و تولیدکننده گراف
- کراولر چند-نخی با محدودیت سرعت
- نمایش گراف تعاملی PyVis
- نرمال‌سازی و اعتبارسنجی URL
- قابلیت خروجی JSON
- ویژگی‌های جستجو و هایلایت در گراف تعاملی
- دابل‌کلیک برای باز کردن URL
- گروه‌بندی نود بر اساس ساب‌دامین
- لی‌اوت سلسله‌مراتبی گراف
- رابط خط فرمان
- نوار پیشرفت با tqdm
- سیستم لاگ جامع
- README دوزبانه (انگلیسی/فارسی)

### برنامه‌ریزی شده
- احترام به robots.txt
- پیکربندی محدودیت عمق
- اعتبارسنجی لینک (تشخیص 404)
- خروجی به فرمت‌های GEXF/GraphML
- پشتیبانی از طرح‌های رنگی سفارشی
