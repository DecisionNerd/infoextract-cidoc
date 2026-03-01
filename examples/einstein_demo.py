#!/usr/bin/env python3
"""
Einstein Biography Demo - Complete infoextract-cidoc Workflow

Demonstrates the full pipeline using Albert Einstein's biography:
1. AI-powered information extraction from text
2. Resolution to stable UUIDs and typed CRM entities
3. Markdown rendering for analysis
4. NetworkX graph construction and analysis
5. Interactive visualization
6. Cypher export for graph databases

Usage:
    GEMINI_API_KEY=... python examples/einstein_demo.py
"""

import asyncio
import os
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv

from infoextract_cidoc.extraction import (
    LangStructExtractor,
    map_to_crm_entities,
    resolve_extraction,
)
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.io.to_markdown import MarkdownStyle, render_table, to_markdown
from infoextract_cidoc.io.to_networkx import (
    calculate_centrality_measures,
    find_communities,
    get_network_statistics,
    to_networkx_graph,
)
from infoextract_cidoc.visualization import (
    create_interactive_plot,
    create_network_summary,
    plot_centrality_network,
    plot_community_network,
    plot_network_graph,
)

load_dotenv()

EINSTEIN_SOURCE = Path(__file__).parent.parent / "src/infoextract_cidoc/examples/einstein.md"
OUTPUT_DIR = Path(__file__).parent / "output" / "einstein"


def check_requirements() -> bool:
    """Check required environment and source files."""
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("LANGSTRUCT_DEFAULT_MODEL"):
        print("Error: set GEMINI_API_KEY or LANGSTRUCT_DEFAULT_MODEL before running.")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return False

    if not EINSTEIN_SOURCE.exists():
        print(f"Error: source file not found: {EINSTEIN_SOURCE}")
        return False

    return True


async def run_demo() -> None:
    """Run the complete Einstein biography demo."""
    print("infoextract-cidoc — Einstein Biography Demo")
    print("=" * 60)

    einstein_text = EINSTEIN_SOURCE.read_text()
    print(f"Loaded Einstein biography ({len(einstein_text)} characters)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: AI-powered Information Extraction
    print("\nStep 1: AI-powered Information Extraction")
    print("-" * 50)

    extractor = LangStructExtractor()
    lite_result = await asyncio.to_thread(extractor.extract, einstein_text)
    extraction_result = resolve_extraction(lite_result)
    crm_entities, crm_relations = map_to_crm_entities(extraction_result)

    print(f"Extracted {len(crm_entities)} entities, {len(crm_relations)} relations")

    entity_types: dict[str, int] = {}
    for entity in crm_entities:
        entity_types[entity.class_code] = entity_types.get(entity.class_code, 0) + 1
    print("Entity breakdown:")
    for class_code, count in sorted(entity_types.items()):
        print(f"  {class_code}: {count}")

    # Step 2: Generate Markdown Reports
    print("\nStep 2: Generate Markdown Reports")
    print("-" * 50)

    markdown_dir = OUTPUT_DIR / "markdown"
    markdown_dir.mkdir(exist_ok=True)

    for i, entity in enumerate(crm_entities[:10]):
        card = to_markdown(entity, MarkdownStyle.CARD)
        slug = entity.label.replace(" ", "_") if entity.label else "unlabelled"
        (markdown_dir / f"entity_{i + 1:02d}_{entity.class_code}_{slug}.md").write_text(card)

    table_md = render_table(crm_entities)
    (markdown_dir / "entities_summary.md").write_text(
        f"# Einstein Biography — CRM Entities Summary\n\n"
        f"Total entities: {len(crm_entities)}\n\n" + table_md
    )

    key_entities = [e for e in crm_entities if e.class_code in {"E21", "E5", "E53"}][:5]
    for entity in key_entities:
        narrative = to_markdown(entity, MarkdownStyle.NARRATIVE)
        slug = (entity.label or "unlabelled").replace(" ", "_")
        (markdown_dir / f"narrative_{entity.class_code}_{slug}.md").write_text(narrative)

    print(f"Markdown reports written to {markdown_dir}")

    # Step 3: NetworkX Graph Construction
    print("\nStep 3: NetworkX Graph Construction")
    print("-" * 50)

    graph = to_networkx_graph(crm_entities)
    print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    # Step 4: Network Analysis
    print("\nStep 4: Network Analysis")
    print("-" * 50)

    centrality_measures = calculate_centrality_measures(graph)
    communities = find_communities(graph)
    network_stats = get_network_statistics(graph)

    print(f"Centrality measures: {list(centrality_measures.keys())}")
    print(f"Communities found: {len(communities)}")

    if centrality_measures.get("degree"):
        top_nodes = sorted(
            centrality_measures["degree"].items(), key=lambda x: x[1], reverse=True
        )[:5]
        print("Most central nodes (degree):")
        for node_id, centrality in top_nodes:
            label = graph.nodes[node_id].get("label", node_id)
            print(f"  {label} ({centrality:.3f})")

    # Step 5: Visualization
    print("\nStep 5: Visualization")
    print("-" * 50)

    plots_dir = OUTPUT_DIR / "plots"
    plots_dir.mkdir(exist_ok=True)

    plot_network_graph(
        graph,
        title="Einstein Biography — CRM Network",
        figsize=(16, 12),
        show_plot=False,
        save_path=str(plots_dir / "network_overview.png"),
    )

    if communities:
        plot_community_network(
            graph,
            communities,
            title="Einstein Biography — Community Structure",
            figsize=(14, 10),
            save_path=str(plots_dir / "community_structure.png"),
        )

    if centrality_measures.get("degree"):
        plot_centrality_network(
            graph,
            centrality_measures["degree"],
            title="Einstein Biography — Degree Centrality",
            centrality_type="degree",
            figsize=(14, 10),
            save_path=str(plots_dir / "degree_centrality.png"),
        )

    interactive_fig = create_interactive_plot(
        graph, title="Einstein Biography — Interactive Network"
    )
    interactive_file = plots_dir / "interactive_network.html"
    interactive_fig.write_html(str(interactive_file))

    print(f"Plots written to {plots_dir}")

    # Step 6: Export to Cypher
    print("\nStep 6: Export to Cypher")
    print("-" * 50)

    cypher_script = generate_cypher_script(crm_entities)
    cypher_file = OUTPUT_DIR / "einstein_network.cypher"
    cypher_file.write_text(
        "// Einstein Biography CRM Network\n"
        "// Generated by infoextract-cidoc\n\n" + cypher_script
    )
    print(f"Cypher script written to {cypher_file}")

    # Step 7: Network Summary
    print("\nStep 7: Network Summary")
    print("-" * 50)

    summary_md = create_network_summary(graph, network_stats)
    (OUTPUT_DIR / "network_summary.md").write_text(summary_md)

    # Final summary
    print("\nDone.")
    print("=" * 60)
    print(f"All outputs in: {OUTPUT_DIR.resolve()}")
    print(f"  Entities:    {len(crm_entities)}")
    print(f"  Relations:   {len(crm_relations)}")
    print(f"  Nodes:       {graph.number_of_nodes()}")
    print(f"  Edges:       {graph.number_of_edges()}")
    print(f"  Communities: {len(communities)}")
    print(f"  Markdown:    {len(list(markdown_dir.glob('*.md')))} files")
    print(f"  Plots:       {len(list(plots_dir.glob('*')))} files")
    print(f"\nOpen interactive network: {interactive_file}")
    print(f"Import to Neo4j/Memgraph: {cypher_file}")


async def main() -> None:
    if not check_requirements():
        sys.exit(1)
    try:
        await run_demo()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nDemo failed: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
