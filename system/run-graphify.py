#!/usr/bin/env python3
"""Run graphify pipeline on the IMPKT workspace."""

import os
import json
import networkx as nx
from pathlib import Path

os.environ['ANTHROPIC_API_KEY'] = 'sk-cp-JL9pwrIqMEe4xtdCEpDAry-nSgo9CIvqeGsm6RTiRELXruKqqB20yBVZWRO-AtVe2_B6u7QIwEQ-TeeSk9QIXBmKa8Qa_yMWQQNapy4gm-zuJvw2uBGMjaE'
os.environ['ANTHROPIC_BASE_URL'] = 'https://api.minimax.chat/v1'
os.environ['ANTHROPIC_MODEL'] = 'MiniMax-M2.7'

from graphify.detect import detect
from graphify.extract import extract, Path as GPath
from graphify.build import build
from graphify.cluster import cluster
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.export import to_json, to_html

os.makedirs('graphify-out', exist_ok=True)
Path('graphify-out/.graphify_python').write_text('C:\\Python314\\python.exe')

root = Path('.')
result = detect(root)

code_files = result['files']['code']
doc_files = result['files']['document']

print(f"Code: {len(code_files)} files")
print(f"Docs: {len(doc_files)} files")

# Extract from code files (AST via tree-sitter)
code_result = {'nodes': [], 'edges': []}
if code_files:
    code_paths = [GPath(f) for f in code_files]
    print(f"\nExtracting code AST from {len(code_paths)} files...")
    code_result = extract(code_paths)
    print(f"  Code extraction: {len(code_result.get('nodes', []))} nodes, {len(code_result.get('edges', []))} edges")

# Extract from docs (headings as nodes, structure as edges)
doc_extractions = []
for f in doc_files:
    p = Path(f)
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Skipping {f}: {e}")
        continue

    nodes = []
    edges = []
    lines = text.split('\n')
    current_heading = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            current_heading = stripped.lstrip('#').strip()
            if current_heading:
                nodes.append({'id': f"{p.name}::{current_heading}", 'label': current_heading,
                              'type': 'heading', 'source': str(p)})
        elif stripped and current_heading:
            if any(kw in stripped for kw in ['TODO', 'NOTE', 'IMPORTANT', 'FIXME', 'WARNING', 'REGLAS', 'TAREA']):
                nid = f"{p.name}::{len(nodes)}"
                nodes.append({'id': nid, 'label': stripped[:100], 'type': 'marker',
                              'source': str(p)})
                edges.append({'source': f"{p.name}::{current_heading}", 'target': nid,
                              'type': 'contains'})

    if nodes:
        doc_extractions.append({'path': str(p), 'nodes': nodes, 'edges': edges})
    print(f"  Doc: {p.name} -> {len(nodes)} nodes, {len(edges)} edges")

# Build graph from code extraction
G = nx.Graph()
for n in code_result.get('nodes', []):
    G.add_node(n['id'], **{k: v for k, v in n.items()})
for e in code_result.get('edges', []):
    G.add_edge(e['source'], e['target'], **{k: v for k, v in e.items()})

print(f"\nCode graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Add doc nodes and edges
for ext in doc_extractions:
    for n in ext['nodes']:
        if not G.has_node(n['id']):
            G.add_node(n['id'], **{k: v for k, v in n.items()})
    for e in ext['edges']:
        if G.has_node(e['source']) and G.has_node(e['target']):
            G.add_edge(e['source'], e['target'], **{k: v for k, v in e.items()})

print(f"Combined graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Cluster
communities = cluster(G)
print(f"Communities: {len(communities)}")

# community labels
community_labels = {cid: f"Community {cid}" for cid in communities}

# Analyze
god = god_nodes(G, top_n=10)
surprises = surprising_connections(G, top_n=10)
questions = suggest_questions(G, communities, community_labels, top_n=5)

# Build simple text report
lines = [
    "# Graph Report - IMPKT Workspace",
    "",
    "## Corpus Check",
    f"- {result['total_files']} files · ~{result['total_words']:,} words",
    "",
    "## Summary",
    f"- {G.number_of_nodes()} nodes · {G.number_of_edges()} edges · {len(communities)} communities detected",
    "",
    "## God Nodes (highest-degree concepts)",
]
for item in god:
    label = item.get('label', item.get('id', '?'))
    degree = item.get('degree', '?')
    lines.append(f"- **{label}** (degree: {degree})")

lines += [
    "",
    "## Surprising Connections",
]
for item in surprises:
    src = item.get('source_label', item.get('source', '?'))
    tgt = item.get('target_label', item.get('target', '?'))
    why = item.get('why', item.get('connection_type', '?'))
    lines.append(f"- **{src}** ↔ **{tgt}**: {why}")

lines += [
    "",
    "## Suggested Questions",
]
for q in questions:
    q_text = q.get('question', q) if isinstance(q, dict) else q
    lines.append(f"- {q_text}")

lines += [
    "",
    "## Communities",
]
for cid, members in communities.items():
    lines.append(f"\n### Community {cid} ({len(members)} nodes)")
    for m in members[:10]:
        lines.append(f"- {m}")
    if len(members) > 10:
        lines.append(f"  ... and {len(members) - 10} more")

report = '\n'.join(lines)
(Path('graphify-out') / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
print(f"\nGRAPH_REPORT.md written ({len(report)} chars)")

# Export
to_json(G, communities, 'graphify-out/graph.json')
print("graph.json exported")

to_html(G, communities, 'graphify-out/graph.html', community_labels)
print("graph.html exported")

print("graph.html exported")