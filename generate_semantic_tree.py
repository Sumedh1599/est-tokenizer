#!/usr/bin/env python3
"""
Generate semantic tree visualization from check_dictionary.csv semantic_frame column
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

def build_semantic_tree(csv_path):
    """Build semantic tree from semantic_frame column"""
    # Tree structure: root_concept -> {words: [], children: []}
    tree = defaultdict(lambda: {'words': [], 'children': defaultdict(list)})
    all_concepts = set()
    
    print("Building semantic tree from semantic_frame column...")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            sanskrit = row.get('sanskrit', '').strip()
            semantic_frame = row.get('semantic_frame', '').strip()
            english = row.get('english', '').strip()
            
            if semantic_frame and sanskrit:
                # Parse semantic_frame - pipe-separated concepts
                # Format: "root_concept | child1 | child2 | ..."
                parts = [p.strip() for p in semantic_frame.split('|') if p.strip()]
                
                if parts:
                    root = parts[0]
                    all_concepts.add(root)
                    
                    # Add word to root node
                    tree[root]['words'].append({
                        'sanskrit': sanskrit,
                        'english': english[:80]  # Truncate
                    })
                    
                    # Build parent-child relationships
                    for i in range(len(parts) - 1):
                        parent = parts[i]
                        child = parts[i + 1]
                        all_concepts.add(child)
                        
                        # Add child to parent's children
                        if child not in tree[parent]['children']:
                            tree[parent]['children'][child] = []
                        tree[parent]['children'][child].append(sanskrit)
            
            count += 1
            if count % 5000 == 0:
                print(f"  Processed {count} rows...")
    
    print(f"\n✅ Tree built from {count} rows")
    print(f"   Unique concepts: {len(all_concepts)}")
    print(f"   Root nodes: {len(tree)}")
    print(f"   Total words: {sum(len(v['words']) for v in tree.values())}")
    
    return dict(tree), all_concepts

def generate_html_tree(tree_data, all_concepts, output_path):
    """Generate interactive HTML tree visualization using D3.js"""
    
    # Prepare simplified tree structure for visualization
    # Focus on top nodes by word count
    sorted_roots = sorted(
        tree_data.items(), 
        key=lambda x: len(x[1]['words']), 
        reverse=True
    )[:100]  # Top 100 roots
    
    # Build hierarchy
    nodes_list = []
    links_list = []
    node_id_map = {}
    node_counter = 1
    
    # Create nodes
    for root, data in sorted_roots:
        if root not in node_id_map:
            node_id_map[root] = node_counter
            nodes_list.append({
                'id': node_counter,
                'name': root[:50],  # Truncate long names
                'word_count': len(data['words']),
                'level': 0
            })
            node_counter += 1
        
        # Add children
        for child, words in list(data['children'].items())[:5]:  # Top 5 children
            if child not in node_id_map:
                node_id_map[child] = node_counter
                nodes_list.append({
                    'id': node_counter,
                    'name': child[:50],
                    'word_count': len(words),
                    'level': 1
                })
                node_counter += 1
            
            # Create link
            links_list.append({
                'source': node_id_map[root],
                'target': node_id_map[child]
            })
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>EST Semantic Tree Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #e2e8f0;
        }}
        .container {{
            max-width: 1800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #7dd3fc;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #94a3b8;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .tree-container {{
            background: rgba(30, 41, 59, 0.7);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(2, 8, 20, 0.4);
            overflow: auto;
        }}
        .node circle {{
            fill: #7dd3fc;
            stroke: #0ea5e9;
            stroke-width: 2px;
            cursor: pointer;
        }}
        .node text {{
            font-size: 11px;
            fill: #e2e8f0;
            pointer-events: none;
        }}
        .link {{
            fill: none;
            stroke: #475569;
            stroke-width: 1.5px;
        }}
        .node:hover circle {{
            fill: #fbbf24;
            stroke: #f59e0b;
        }}
        .tooltip {{
            position: absolute;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid #7dd3fc;
            border-radius: 8px;
            padding: 12px;
            color: #e2e8f0;
            font-size: 12px;
            pointer-events: none;
            display: none;
            max-width: 300px;
            z-index: 1000;
        }}
        .stats {{
            text-align: center;
            color: #94a3b8;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🕉️ EST Semantic Tree Visualization</h1>
        <div class="subtitle">Semantic concept hierarchy from check_dictionary.csv</div>
        <div class="stats">
            <strong>Total Nodes:</strong> {len(nodes_list)} | 
            <strong>Total Links:</strong> {len(links_list)} | 
            <strong>Top 100 Root Concepts</strong>
        </div>
        <div class="tree-container">
            <svg id="tree-svg" width="1700" height="1200"></svg>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        const nodes = {json.dumps(nodes_list)};
        const links = {json.dumps(links_list)};
        
        const svg = d3.select("#tree-svg");
        const width = 1700;
        const height = 1200;
        const tooltip = d3.select("#tooltip");
        
        // Create tree layout
        const tree = d3.tree()
            .size([height - 150, width - 300]);
        
        // Build hierarchy
        const nodeMap = new Map();
        nodes.forEach(d => {{
            nodeMap.set(d.id, {{...d, children: []}});
        }});
        
        // Build tree structure
        const rootNodes = nodes.filter(d => d.level === 0);
        const rootData = {{id: 0, name: "Semantic Roots", children: []}};
        
        rootNodes.forEach(root => {{
            const rootNode = nodeMap.get(root.id);
            // Find children
            links.forEach(link => {{
                if (link.source === root.id) {{
                    const child = nodeMap.get(link.target);
                    if (child && !rootNode.children.includes(child)) {{
                        rootNode.children.push(child);
                    }}
                }}
            }});
            rootData.children.push(rootNode);
        }});
        
        const root = d3.hierarchy(rootData);
        tree(root);
        
        // Draw links
        svg.selectAll(".link")
            .data(root.links())
            .enter()
            .append("path")
            .attr("class", "link")
            .attr("d", d3.linkHorizontal()
                .x(d => d.y + 150)
                .y(d => d.x + 75));
        
        // Draw nodes
        const node = svg.selectAll(".node")
            .data(root.descendants().filter(d => d.data.id !== 0))
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${{d.y + 150}},${{d.x + 75}})`);
        
        node.append("circle")
            .attr("r", d => Math.min(Math.sqrt(d.data.word_count || 1) * 2 + 8, 25))
            .on("mouseover", function(event, d) {{
                tooltip.style("display", "block")
                    .html(`<strong>${{d.data.name}}</strong><br/>Words: ${{d.data.word_count || 0}}<br/>Level: ${{d.data.level}}`)
                    .style("left", (event.pageX + 15) + "px")
                    .style("top", (event.pageY - 10) + "px");
            }})
            .on("mouseout", function() {{
                tooltip.style("display", "none");
            }});
        
        node.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -15 : 15)
            .style("text-anchor", d => d.children ? "end" : "start")
            .text(d => d.data.name.length > 25 ? d.data.name.substring(0, 22) + "..." : d.data.name);
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML tree visualization generated: {output_path}")

def generate_text_tree(tree_data, root_nodes, output_path):
    """Generate text-based tree visualization"""
    
    output = []
    output.append("=" * 100)
    output.append("EST SEMANTIC TREE VISUALIZATION")
    output.append("=" * 100)
    output.append(f"\nTotal Root Concepts: {len(tree_data)}")
    output.append(f"Total Unique Concepts: {len(root_nodes)}")
    output.append("\n" + "=" * 100 + "\n")
    
    # Show top nodes by word count
    sorted_roots = sorted(
        tree_data.items(), 
        key=lambda x: len(x[1]['words']), 
        reverse=True
    )
    
    for i, (root, data) in enumerate(sorted_roots[:100], 1):  # Top 100
        words = data['words']
        children = list(data['children'].keys())
        
        output.append(f"\n[{i}] {root}")
        output.append(f"    📚 Words: {len(words)}")
        
        if words:
            output.append(f"    Sample Sanskrit words:")
            for word in words[:5]:
                sanskrit = word['sanskrit']
                english = word['english'][:70]
                output.append(f"      • {sanskrit}: {english}")
        
        if children:
            output.append(f"    🌿 Child concepts ({len(children)}): {', '.join(children[:8])}")
            if len(children) > 8:
                output.append(f"      ... and {len(children) - 8} more")
        
        output.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"✅ Text tree visualization generated: {output_path}")

def main():
    csv_path = Path('data/check_dictionary.csv')
    
    if not csv_path.exists():
        print(f"❌ Error: {csv_path} not found")
        return
    
    # Build tree
    tree_data, all_concepts = build_semantic_tree(csv_path)
    
    # Generate visualizations
    generate_html_tree(tree_data, all_concepts, 'semantic_tree.html')
    generate_text_tree(tree_data, all_concepts, 'semantic_tree.txt')
    
    # Save JSON data (sample)
    tree_json = {
        'total_concepts': len(all_concepts),
        'total_roots': len(tree_data),
        'top_roots': [
            {
                'concept': root,
                'word_count': len(data['words']),
                'sample_words': data['words'][:3],
                'children_count': len(data['children']),
                'sample_children': list(data['children'].keys())[:5]
            }
            for root, data in sorted(
                tree_data.items(), 
                key=lambda x: len(x[1]['words']), 
                reverse=True
            )[:50]
        ]
    }
    
    with open('semantic_tree_data.json', 'w', encoding='utf-8') as f:
        json.dump(tree_json, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON data saved: semantic_tree_data.json")
    print(f"\n📊 Summary:")
    print(f"   - Unique concepts: {len(all_concepts)}")
    print(f"   - Root concepts: {len(tree_data)}")
    print(f"   - Total words mapped: {sum(len(v['words']) for v in tree_data.values())}")

if __name__ == "__main__":
    main()
