#!/usr/bin/env python3
"""
Process news articles from JSON file and perform clustering
"""
import json
import argparse
from pathlib import Path
from typing import List

from app.models.article import Article, ClusteringRequest
from app.services.news_clustering import NewsClusteringService


def process_json_file(json_path: str, output_path: str = None):
    """
    Load news data from JSON file and perform clustering
    
    Args:
        json_path: Path to input JSON file
        output_path: Optional path for output JSON file
    """
    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate and convert to Article objects
    articles = []
    if isinstance(data, list):
        # If data is a list of articles
        for item in data:
            if isinstance(item, dict) and 'id' in item and 'content' in item:
                articles.append(Article(id=item['id'], content=item['content']))
    elif isinstance(data, dict) and 'articles' in data:
        # If data follows the API request format
        for item in data['articles']:
            articles.append(Article(id=item['id'], content=item['content']))
    else:
        raise ValueError("Invalid JSON format. Expected list of articles or dict with 'articles' key")
    
    if not articles:
        print("No articles found in the JSON file")
        return
    
    print(f"Processing {len(articles)} articles...")
    
    # Create clustering request
    request = ClusteringRequest(articles=articles)
    
    # Initialize service and process articles
    service = NewsClusteringService()
    try:
        clusters = service.process_articles(request.articles)
        
        # Prepare output
        output_data = {
            "total_articles": len(articles),
            "total_clusters": len(clusters),
            "clusters": [
                {
                    "cluster_id": cluster.cluster_id,
                    "articles": cluster.articles,
                    "topic_title": cluster.topic_title,
                    "topic_summary": cluster.topic_summary,
                    "article_count": len(cluster.articles)
                }
                for cluster in clusters
            ]
        }
        
        # Save to output file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {output_path}")
        else:
            # Print results to console
            print(f"\nClustering Results:")
            print(f"Total clusters found: {len(clusters)}")
            for cluster in clusters:
                print(f"\nCluster {cluster.cluster_id}:")
                print(f"  Title: {cluster.topic_title}")
                print(f"  Summary: {cluster.topic_summary}")
                print(f"  Articles: {len(cluster.articles)} articles")
                print(f"  Article IDs: {', '.join(cluster.articles[:5])}", end="")
                if len(cluster.articles) > 5:
                    print(f"... and {len(cluster.articles) - 5} more")
                else:
                    print()
    
    except Exception as e:
        print(f"Error processing articles: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Process news articles from JSON file and perform clustering"
    )
    parser.add_argument(
        "input",
        help="Path to input JSON file containing news articles"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output JSON file (optional)",
        default=None
    )
    parser.add_argument(
        "-s", "--show",
        help="Show output JSON file content after processing",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Verify input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        return
    
    # Run function
    process_json_file(args.input, args.output)
    
    # Show output file if requested
    if args.output and args.show:
        print("\n" + "="*60)
        print("Output file contents:")
        print("="*60)
        with open(args.output, 'r', encoding='utf-8') as f:
            print(json.dumps(json.load(f), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()