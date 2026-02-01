#!/usr/bin/env python3
"""
Integrated Web Crawler & Interactive Graph Generator
Combines web crawling with interactive PyVis graph visualization

Author: Mehrab Mahmoudifar
GitHub: https://github.com/mehrabmahmoudifar
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs, urlencode, unquote
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import json
import logging
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Set, Dict, List, Tuple, Optional
import sys
import os
from pyvis.network import Network

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawl_log.txt', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# Section 1: Web Crawler
# ==========================================
class WebCrawler:
    """
    Web crawler that discovers and maps internal links within a domain.
    Implements rate limiting, retry logic, and URL normalization.
    """
    
    def __init__(self, start_url: str, max_workers: int = 5, rate_limit: float = 1.0):
        """
        Initialize the web crawler.
        
        Args:
            start_url: The URL to start crawling from
            max_workers: Maximum number of concurrent threads
            rate_limit: Minimum time between requests in seconds
        """
        self.start_url = start_url
        self.parsed_start = urlparse(start_url)
        self.domain = self.parsed_start.netloc
        self.base_domain = self._extract_base_domain(self.domain)
        self.visited: Set[str] = set()
        self.to_visit: Set[str] = {start_url}
        self.graph = nx.DiGraph()
        self.page_content: Dict[str, str] = {}
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        logger.info(f"Crawler initialized - Domain: {self.domain}")
    
    def _extract_base_domain(self, domain: str) -> str:
        """Extract the base domain from a full domain name."""
        parts = domain.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return domain
    
    def _normalize_url(self, url: str, base_url: str = None) -> Optional[str]:
        """
        Normalize and validate URLs.
        
        Args:
            url: The URL to normalize
            base_url: Base URL for resolving relative URLs
            
        Returns:
            Normalized URL or None if invalid
        """
        try:
            url = url.strip()
            # Skip non-HTTP protocols
            if url.startswith(('javascript:', 'mailto:', 'tel:', 'data:', '#')):
                return None
            
            # Resolve relative URLs
            if base_url:
                url = urljoin(base_url, url)
            
            parsed = urlparse(url)
            
            # Only HTTP/HTTPS allowed
            if parsed.scheme not in ('http', 'https'):
                return None
            
            # Only internal URLs
            if not self._is_internal_url(url):
                return None
            
            # Normalize query parameters
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            sorted_query = urlencode(sorted(query_params.items()), doseq=True)
            
            # Reconstruct normalized URL
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc.lower(),
                parsed.path or '/',
                parsed.params,
                sorted_query,
                ''
            ))
            
            # Remove trailing slash except for root
            if normalized.endswith('/') and normalized.count('/') > 3:
                normalized = normalized[:-1]
            
            return normalized
        except Exception:
            return None
    
    def _is_internal_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        try:
            parsed = urlparse(url)
            url_domain = parsed.netloc.lower()
            return (url_domain == self.domain.lower() or 
                    url_domain.endswith('.' + self.base_domain.lower()))
        except:
            return False
    
    def _fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        """
        Fetch page content with retry logic and rate limiting.
        
        Args:
            url: URL to fetch
            retries: Number of retry attempts
            
        Returns:
            HTML content or None if failed
        """
        for attempt in range(retries):
            try:
                # Rate limiting
                elapsed = time.time() - self.last_request_time
                if elapsed < self.rate_limit:
                    time.sleep(self.rate_limit - elapsed)
                
                self.last_request_time = time.time()
                
                response = self.session.get(url, timeout=15, allow_redirects=True)
                
                if response.status_code == 200:
                    if 'text/html' in response.headers.get('content-type', '').lower():
                        return response.text
                elif response.status_code in (404, 410):
                    return None
                    
            except requests.exceptions.RequestException:
                pass
            
            # Exponential backoff
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
        
        return None
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract and normalize all links from HTML content.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            List of normalized URLs
        """
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check for base tag
            base_tag = soup.find('base', href=True)
            if base_tag:
                base_url = urljoin(base_url, base_tag['href'])
            
            # Extract all anchor tags
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                normalized = self._normalize_url(href, base_url)
                if normalized and normalized not in self.visited:
                    links.append(normalized)
        except Exception:
            pass
        
        return links
    
    def _crawl_url(self, url: str) -> Tuple[str, List[str]]:
        """
        Crawl a single URL and extract its links.
        
        Args:
            url: URL to crawl
            
        Returns:
            Tuple of (url, list of extracted links)
        """
        html = self._fetch_page(url)
        if html is None:
            return url, []
        
        links = self._extract_links(html, url)
        return url, links
    
    def crawl(self) -> nx.DiGraph:
        """
        Execute the crawling process using concurrent threads.
        
        Returns:
            NetworkX DiGraph representing the website structure
        """
        logger.info(f"Starting crawl from: {self.start_url}")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            with tqdm(desc="Crawling pages", unit="page") as pbar:
                while self.to_visit:
                    # Prepare batch of URLs
                    batch = []
                    while self.to_visit and len(batch) < self.max_workers * 2:
                        url = self.to_visit.pop()
                        if url not in self.visited:
                            batch.append(url)
                            self.visited.add(url)
                    
                    if not batch:
                        break
                    
                    # Submit crawl tasks
                    futures = {executor.submit(self._crawl_url, url): url for url in batch}
                    
                    # Process completed tasks
                    for future in as_completed(futures):
                        try:
                            source_url, links = future.result()
                            
                            # Add to graph
                            self.graph.add_node(source_url)
                            for link in links:
                                self.graph.add_edge(source_url, link)
                                if link not in self.visited:
                                    self.to_visit.add(link)
                            
                            # Update progress
                            pbar.update(1)
                            pbar.set_postfix({
                                'nodes': self.graph.number_of_nodes(),
                                'edges': self.graph.number_of_edges()
                            })
                        except Exception:
                            pass
        
        return self.graph

# ==========================================
# Section 2: Statistics Generator
# ==========================================
class StatsGenerator:
    """Generate and save statistics and data from the crawled graph."""
    
    def __init__(self, graph: nx.DiGraph, start_url: str):
        """
        Initialize the stats generator.
        
        Args:
            graph: NetworkX graph from crawler
            start_url: Starting URL of the crawl
        """
        self.graph = graph
        self.start_url = start_url
    
    def save_stats(self, filename: str) -> Dict:
        """
        Save basic statistics to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            Dictionary containing statistics
        """
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'start_url': self.start_url
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return stats
    
    def save_links(self, filename: str) -> List[Dict]:
        """
        Save detailed link information to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            List of dictionaries containing link data
        """
        in_degree = dict(self.graph.in_degree())
        out_degree = dict(self.graph.out_degree())
        
        links_data = []
        for node in self.graph.nodes():
            links_data.append({
                'url': node,
                'in_degree': in_degree[node],
                'out_degree': out_degree[node],
                'outgoing_links': list(self.graph.successors(node))
            })
        
        # Sort by outgoing links
        links_data.sort(key=lambda x: x['out_degree'], reverse=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to file: {filename}")
        return links_data

# ==========================================
# Section 3: Interactive Visualization
# ==========================================
class InteractiveGraphGenerator:
    """Generate interactive PyVis network visualization."""
    
    def __init__(self, data_list: List[Dict]):
        """
        Initialize the graph generator.
        
        Args:
            data_list: List of link data from StatsGenerator
        """
        self.data_json = data_list

    def get_node_info(self, url: str) -> Tuple[str, str, str]:
        """
        Extract display information from URL.
        
        Args:
            url: URL to process
            
        Returns:
            Tuple of (label, group, decoded_url)
        """
        decoded_url = unquote(url)
        parsed = urlparse(decoded_url)
        domain = parsed.netloc
        path = parsed.path
        
        # Create label from path or domain
        if path == "" or path == "/":
            label = domain
        else:
            label = path if len(path) < 30 else path[:15] + "..." + path[-10:]
        
        # Determine group based on subdomain
        parsed_original = urlparse(url)
        domain_original = parsed_original.netloc
        
        if "mag." in domain_original:
            group = "Mag"
        elif "business." in domain_original:
            group = "Business"
        elif "cloud." in domain_original:
            group = "Cloud"
        elif "shop." in domain_original:
            group = "Shop"
        elif "my." in domain_original:
            group = "Panel"
        else:
            group = "Main"
        
        return label, group, decoded_url

    def generate(self, output_filename: str):
        """
        Generate interactive HTML graph visualization.
        
        Args:
            output_filename: Output HTML filename
        """
        logger.info("Creating interactive PyVis graph...")
        
        net = Network(
            height="95vh",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            directed=True
        )

        # Color mapping for different groups
        color_map = {
            "Mag": "#E91E63",
            "Business": "#4CAF50",
            "Cloud": "#2196F3",
            "Shop": "#FF9800",
            "Panel": "#9C27B0",
            "Main": "#212121"
        }

        # Build nodes and edges
        for entry in self.data_json:
            source_url = entry['url']
            src_label, src_group, src_decoded = self.get_node_info(source_url)
            
            # Add source node
            net.add_node(
                source_url,
                label=src_label,
                title=src_decoded,
                group=src_group,
                color=color_map.get(src_group, "gray"),
                shape="box",
                font={'size': 16, 'face': 'Tahoma'}
            )
            
            # Add target nodes and edges
            for target_url in entry.get('outgoing_links', []):
                trg_label, trg_group, trg_decoded = self.get_node_info(target_url)
                
                net.add_node(
                    target_url,
                    label=trg_label,
                    title=trg_decoded,
                    group=trg_group,
                    color=color_map.get(trg_group, "gray"),
                    shape="box"
                )
                
                net.add_edge(source_url, target_url, color="#bdbdbd")

        # Configure graph options
        options = {
            "layout": {
                "hierarchical": {
                    "enabled": True,
                    "levelSeparation": 350,
                    "nodeSpacing": 60,
                    "treeSpacing": 200,
                    "blockShifting": True,
                    "edgeMinimization": True,
                    "parentCentralization": False,
                    "direction": "LR",
                    "sortMethod": "directed"
                }
            },
            "physics": {"enabled": False},
            "interaction": {
                "hover": True,
                "navigationButtons": True,
                "keyboard": True,
                "multiselect": True
            },
            "edges": {
                "smooth": {
                    "type": "cubicBezier",
                    "forceDirection": "horizontal",
                    "roundness": 0.4
                },
                "arrows": {"to": {"enabled": True, "scaleFactor": 0.5}},
                "color": {"inherit": False}
            }
        }
        net.set_options(json.dumps(options))
        
        # Save raw HTML
        net.save_graph(output_filename)
        
        # Inject custom JavaScript
        self._inject_js(output_filename)
        logger.info(f"Interactive graph ready: {output_filename}")

    def _inject_js(self, filename: str):
        """
        Inject custom JavaScript for search, highlighting, and double-click functionality.
        
        Args:
            filename: HTML file to modify
        """
        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()

        custom_script = """
        <style>
            #search-container {
                position: absolute; top: 20px; left: 20px; z-index: 1000;
                background: white; padding: 10px; border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2); font-family: Tahoma, sans-serif;
            }
            #node-search { padding: 8px; width: 300px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; direction: ltr; }
            #search-btn { padding: 8px 15px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
            #search-btn:hover { background: #1976D2; }
            #reset-btn {
                position: absolute; bottom: 20px; right: 20px; z-index: 1000;
                padding: 10px 20px; background: #f44336; color: white; border: none;
                border-radius: 5px; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                display: none; font-family: Tahoma, sans-serif;
            }
        </style>

        <div id="search-container">
            <label for="node-search">Search (link or name):</label><br>
            <input type="text" id="node-search" list="nodes-datalist" placeholder="Search...">
            <datalist id="nodes-datalist"></datalist>
            <button id="search-btn">Go</button>
        </div>
        <button id="reset-btn" onclick="resetGraph()">Reset View</button>

        <script>
            var allNodes = nodes.get(); 
            var datalist = document.getElementById('nodes-datalist');
            
            allNodes.forEach(function(node) {
                var option = document.createElement('option');
                option.value = node.title; 
                datalist.appendChild(option);
            });

            document.getElementById('search-btn').addEventListener('click', function() {
                var inputVal = document.getElementById('node-search').value;
                var foundNode = allNodes.find(n => n.label === inputVal || n.title === inputVal || n.id === inputVal);
                
                if (foundNode) {
                    network.focus(foundNode.id, {scale: 1.5, animation: true});
                    network.selectNodes([foundNode.id]);
                    highlightNode(foundNode.id);
                } else {
                    alert('Node not found!');
                }
            });

            // Double-click to open link in new tab
            network.on("doubleClick", function (params) {
                if (params.nodes.length > 0) {
                    var selectedNodeId = params.nodes[0];
                    window.open(selectedNodeId, '_blank');
                }
            });

            // Right-click alternative
            network.on("oncontextmenu", function (params) {
                params.event.preventDefault(); 
                var selectedNodeId = network.getNodeAt(params.pointer.DOM);
                if (selectedNodeId) { window.open(selectedNodeId, '_blank'); }
            });

            // Single click for highlighting
            network.on("click", function (params) {
                if (params.nodes.length > 0) { highlightNode(params.nodes[0]); }
            });

            function highlightNode(selectedNodeId) {
                var connectedNodes = network.getConnectedNodes(selectedNodeId);
                var allNodeIds = nodes.getIds();
                
                // Dim all nodes
                var updateArray = [];
                allNodeIds.forEach(function(id) {
                    updateArray.push({id: id, color: {background: 'rgba(200,200,200,0.2)', border: 'rgba(200,200,200,0.2)'}, font: {color: 'rgba(200,200,200,0.2)'}});
                });
                nodes.update(updateArray);
                
                // Dim all edges
                var edgeUpdates = [];
                var allEdges = edges.get();
                allEdges.forEach(function(edge) {
                    edgeUpdates.push({id: edge.id, color: {color: 'rgba(230,230,230,0.1)', opacity: 0.1}});
                });
                edges.update(edgeUpdates);

                // Highlight selected and connected nodes
                var highlightNodes = [selectedNodeId].concat(connectedNodes);
                var highlightUpdates = [];
                
                highlightNodes.forEach(function(id) {
                    highlightUpdates.push({id: id, color: {background: '#FFEB3B', border: '#000'}, font: {color: 'black'}});
                });
                nodes.update(highlightUpdates);

                // Highlight connected edges
                var connectedEdges = network.getConnectedEdges(selectedNodeId);
                var connectedEdgeUpdates = [];
                
                connectedEdges.forEach(function(edgeId) {
                    var edge = edges.get(edgeId);
                    if(edge.from === selectedNodeId) {
                        connectedEdgeUpdates.push({id: edgeId, color: {color: 'red', opacity: 1}, width: 2});
                    } else {
                        connectedEdgeUpdates.push({id: edgeId, color: {color: 'blue', opacity: 1}, width: 2});
                    }
                });
                edges.update(connectedEdgeUpdates);
                
                document.getElementById('reset-btn').style.display = 'block';
            }

            function resetGraph() { location.reload(); }
        </script>
        </body>
        """
        
        html_content = html_content.replace('</body>', custom_script)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)


# ==========================================
# Main: Input Management and Execution
# ==========================================

def get_safe_filename_base(url: str) -> str:
    """
    Convert URL to safe filename base.
    
    Args:
        url: URL to convert
        
    Returns:
        Safe filename string
    """
    parsed = urlparse(url)
    # Remove www and replace dots with underscores
    name = parsed.netloc.replace('www.', '').replace('.', '_').replace(':', '')
    if not name:
        name = "output"
    return name

def main():
    """Main execution function."""
    print("=" * 70)
    print("WEB CRAWLER & INTERACTIVE GRAPH GENERATOR")
    print("Author: Mehrab Mahmoudifar")
    print("=" * 70)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web Crawler & Graph Generator')
    parser.add_argument('url', nargs='?', help='Starting URL to crawl')
    args = parser.parse_args()

    target_url = args.url
    
    # If no argument provided, ask user
    if not target_url:
        target_url = input("Please enter website URL (example: https://example.com): ").strip()
        if not target_url:
            print("No URL provided. Exiting.")
            sys.exit(1)
            
    # Ensure URL has protocol
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # Generate output filenames
    base_name = get_safe_filename_base(target_url)
    
    json_filename = f"{base_name}_links.json"
    html_filename = f"{base_name}_interactive.html"
    stats_filename = f"{base_name}_stats.json"
    
    print(f"Target: {target_url}")
    print(f"Base Filename: {base_name}")
    print("-" * 70)

    try:
        # Step 1: Crawl website
        crawler = WebCrawler(target_url, max_workers=5)
        graph = crawler.crawl()
        
        # Step 2: Save data
        stats_gen = StatsGenerator(graph, target_url)
        stats_gen.save_stats(stats_filename)
        
        links_data = stats_gen.save_links(json_filename)
        
        # Step 3: Generate interactive visualization
        if links_data:
            visualizer = InteractiveGraphGenerator(links_data)
            visualizer.generate(html_filename)
            
            print("\n" + "=" * 70)
            print("Operation completed successfully!")
            print(f"Output files for {base_name}:")
            print(f"  1. {html_filename} (Interactive graph - main file)")
            print(f"  2. {json_filename} (Raw data)")
            print(f"  3. {stats_filename} (Statistics)")
            print("=" * 70)
        else:
            print("No links found, graph will not be generated.")

    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
