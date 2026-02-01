#!/usr/bin/env python3
"""
Example usage of Web Crawler & Graph Generator
Author: Mehrab Mahmoudifar
"""

from crawler import WebCrawler, StatsGenerator, InteractiveGraphGenerator

def example_basic_crawl():
    """Example 1: Basic crawling"""
    print("Example 1: Basic Crawl")
    print("-" * 50)
    
    # Initialize crawler
    crawler = WebCrawler(
        start_url="https://example.com",
        max_workers=5,
        rate_limit=1.0
    )
    
    # Execute crawl
    graph = crawler.crawl()
    
    # Generate stats
    stats_gen = StatsGenerator(graph, "https://example.com")
    stats = stats_gen.save_stats("example_stats.json")
    
    print(f"Nodes found: {stats['nodes']}")
    print(f"Edges found: {stats['edges']}")
    print()

def example_custom_visualization():
    """Example 2: Custom visualization settings"""
    print("Example 2: Custom Visualization")
    print("-" * 50)
    
    # Crawl
    crawler = WebCrawler("https://example.com", max_workers=3)
    graph = crawler.crawl()
    
    # Generate data
    stats_gen = StatsGenerator(graph, "https://example.com")
    links_data = stats_gen.save_links("example_links.json")
    
    # Create visualization
    visualizer = InteractiveGraphGenerator(links_data)
    visualizer.generate("example_graph.html")
    
    print("Interactive graph created: example_graph.html")
    print()

def example_multiple_sites():
    """Example 3: Crawl multiple sites"""
    print("Example 3: Multiple Sites")
    print("-" * 50)
    
    sites = [
        "https://example1.com",
        "https://example2.com",
        "https://example3.com"
    ]
    
    for site in sites:
        print(f"Crawling: {site}")
        
        crawler = WebCrawler(site, max_workers=5)
        graph = crawler.crawl()
        
        # Generate unique filenames
        domain = site.replace('https://', '').replace('http://', '').replace('.', '_')
        
        stats_gen = StatsGenerator(graph, site)
        stats_gen.save_stats(f"{domain}_stats.json")
        links_data = stats_gen.save_links(f"{domain}_links.json")
        
        visualizer = InteractiveGraphGenerator(links_data)
        visualizer.generate(f"{domain}_graph.html")
        
        print(f"Completed: {domain}")
        print()

if __name__ == '__main__':
    # Run examples
    # Uncomment the example you want to run
    
    # example_basic_crawl()
    # example_custom_visualization()
    # example_multiple_sites()
    
    print("Examples ready to run!")
    print("Uncomment the example you want to execute in the code.")
