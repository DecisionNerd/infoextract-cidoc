#!/usr/bin/env python3
"""
Einstein Biography Demo - Complete COLLIE Workflow

This script demonstrates the complete COLLIE workflow using Albert Einstein's biography:
1. AI-powered information extraction from text
2. Conversion to CIDOC CRM entities
3. Markdown rendering for analysis
4. NetworkX graph construction and analysis
5. Interactive visualization
6. Cypher export for graph databases

Usage:
    python einstein_demo.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv

from infoextract_cidoc.extraction import InformationExtractor
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table
from infoextract_cidoc.io.to_networkx import (
    to_networkx_graph,
    calculate_centrality_measures,
    find_communities,
    get_network_statistics
)
from infoextract_cidoc.visualization import (
    plot_network_graph,
    create_interactive_plot,
    create_network_summary,
    plot_community_network,
    plot_centrality_network
)
from infoextract_cidoc.io.to_cypher import generate_cypher_script

# Load environment variables
load_dotenv()


def check_requirements():
    """Check if all requirements are met."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY environment variable is required.")
        print("Please set your Google API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        print("Or create a .env file with:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        return False
    
    einstein_file = Path("src/infoextract_cidoc/examples/einstein.md")
    if not einstein_file.exists():
        print(f"❌ Error: Einstein file not found: {einstein_file}")
        return False
    
    return True


async def einstein_complete_demo():
    """Run the complete Einstein biography demo."""
    print("🧠 COLLIE Einstein Biography Demo")
    print("=" * 60)
    print("Demonstrating complete workflow: Text → AI → CRM → NetworkX → Visualization")
    print("=" * 60)
    
    # Read Einstein biography
    einstein_file = Path("src/infoextract_cidoc/examples/einstein.md")
    with open(einstein_file, "r") as f:
        einstein_text = f.read()
    
    print(f"📖 Loaded Einstein biography ({len(einstein_text)} characters)")
    
    # Create output directory
    output_dir = Path("einstein_demo_output")
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: AI-powered Information Extraction
    print("\n🤖 Step 1: AI-powered Information Extraction")
    print("-" * 50)
    
    try:
        extractor = InformationExtractor()
        extraction_result = await extractor.extract_from_text(einstein_text)
        
        print(f"✅ Extracted {len(extraction_result.entities)} entities")
        print(f"✅ Extracted {len(extraction_result.relationships)} relationships")
        
        # Show entity breakdown by type
        entity_types = {}
        for entity in extraction_result.entities:
            entity_types[entity.class_code] = entity_types.get(entity.class_code, 0) + 1
        
        print("\n📊 Entity Breakdown:")
        for class_code, count in entity_types.items():
            print(f"  - {class_code}: {count} entities")
            
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return
    
    # Step 2: Convert to CRM Entities
    print("\n🏗️ Step 2: Convert to CRM Entities")
    print("-" * 50)
    
    from infoextract_cidoc.models.base import CRMEntity
    
    crm_entities = []
    for entity in extraction_result.entities:
        crm_entity = CRMEntity(
            id=str(entity.id),
            class_code=entity.class_code,
            label=entity.label,
            notes=entity.description,
            type=[entity.class_code]
        )
        crm_entities.append(crm_entity)
    
    print(f"✅ Created {len(crm_entities)} CRM entities")
    
    # Step 3: Generate Markdown Reports
    print("\n📄 Step 3: Generate Markdown Reports")
    print("-" * 50)
    
    markdown_dir = output_dir / "markdown"
    markdown_dir.mkdir(exist_ok=True)
    
    # Individual entity cards
    for i, entity in enumerate(crm_entities[:10]):  # Show first 10 entities
        markdown_card = to_markdown(entity, MarkdownStyle.CARD)
        card_file = markdown_dir / f"entity_{i+1:02d}_{entity.class_code}_{entity.label.replace(' ', '_')}.md"
        with open(card_file, "w") as f:
            f.write(markdown_card)
    
    # Summary table
    table_markdown = render_table(crm_entities)
    table_file = markdown_dir / "entities_summary.md"
    with open(table_file, "w") as f:
        f.write("# Einstein Biography - CRM Entities Summary\n\n")
        f.write(f"Total entities extracted: {len(crm_entities)}\n\n")
        f.write(table_markdown)
    
    # Detailed narrative for key entities
    key_entities = [e for e in crm_entities if e.class_code in ["E21", "E5", "E53"]][:5]
    for entity in key_entities:
        narrative = to_markdown(entity, MarkdownStyle.NARRATIVE)
        narrative_file = markdown_dir / f"narrative_{entity.class_code}_{entity.label.replace(' ', '_')}.md"
        with open(narrative_file, "w") as f:
            f.write(f"# {entity.label} - Narrative\n\n")
            f.write(narrative)
    
    print(f"✅ Generated Markdown reports in {markdown_dir}")
    
    # Step 4: NetworkX Graph Construction
    print("\n🕸️ Step 4: NetworkX Graph Construction")
    print("-" * 50)
    
    graph = to_networkx_graph(crm_entities)
    
    print(f"✅ Created NetworkX graph:")
    print(f"  - Nodes: {graph.number_of_nodes()}")
    print(f"  - Edges: {graph.number_of_edges()}")
    print(f"  - Density: {graph.density():.3f}")
    
    # Step 5: Network Analysis
    print("\n📊 Step 5: Network Analysis")
    print("-" * 50)
    
    # Calculate centrality measures
    centrality_measures = calculate_centrality_measures(graph)
    
    # Find communities
    communities = find_communities(graph)
    
    # Get comprehensive network statistics
    network_stats = get_network_statistics(graph)
    
    print(f"✅ Centrality measures calculated: {list(centrality_measures.keys())}")
    print(f"✅ Found {len(communities)} communities")
    print(f"✅ Network statistics computed")
    
    # Show most central nodes
    if centrality_measures.get("degree"):
        degree_centrality = centrality_measures["degree"]
        top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n🔝 Most Central Nodes (by degree):")
        for node_id, centrality in top_nodes:
            node_data = graph.nodes[node_id]
            label = node_data.get("label", node_id)
            print(f"  - {label} (centrality: {centrality:.3f})")
    
    # Step 6: Visualization
    print("\n🎨 Step 6: Visualization")
    print("-" * 50)
    
    plots_dir = output_dir / "plots"
    plots_dir.mkdir(exist_ok=True)
    
    # Static network plot
    fig = plot_network_graph(
        graph,
        title="Einstein Biography - CRM Network Analysis",
        figsize=(16, 12),
        show_plot=False,
        save_path=str(plots_dir / "network_overview.png")
    )
    
    # Community structure plot
    if communities:
        community_fig = plot_community_network(
            graph,
            communities,
            title="Einstein Biography - Community Structure",
            figsize=(14, 10),
            save_path=str(plots_dir / "community_structure.png")
        )
    
    # Centrality plot
    if centrality_measures.get("degree"):
        centrality_fig = plot_centrality_network(
            graph,
            centrality_measures["degree"],
            title="Einstein Biography - Degree Centrality",
            centrality_type="degree",
            figsize=(14, 10),
            save_path=str(plots_dir / "degree_centrality.png")
        )
    
    # Interactive plot
    interactive_fig = create_interactive_plot(
        graph,
        title="Einstein Biography - Interactive Network",
        show_labels=True
    )
    
    # Save interactive plot
    interactive_file = plots_dir / "interactive_network.html"
    interactive_fig.write_html(str(interactive_file))
    
    print(f"✅ Generated static plots in {plots_dir}")
    print(f"✅ Generated interactive plot: {interactive_file}")
    
    # Step 7: Export to Cypher
    print("\n🔗 Step 7: Export to Cypher")
    print("-" * 50)
    
    cypher_script = generate_cypher_script(crm_entities)
    cypher_file = output_dir / "einstein_network.cypher"
    with open(cypher_file, "w") as f:
        f.write("-- Einstein Biography CRM Network\n")
        f.write("-- Generated by COLLIE\n\n")
        f.write(cypher_script)
    
    print(f"✅ Generated Cypher script: {cypher_file}")
    
    # Step 8: Create Comprehensive Report
    print("\n📋 Step 8: Create Comprehensive Report")
    print("-" * 50)
    
    report_file = output_dir / "einstein_analysis_report.md"
    with open(report_file, "w") as f:
        f.write("# Einstein Biography - COLLIE Analysis Report\n\n")
        f.write("## Overview\n\n")
        f.write("This report presents a comprehensive analysis of Albert Einstein's biography ")
        f.write("using the COLLIE (Classful Ontology for Life-Events Information Extraction) ")
        f.write("workflow, which combines AI-powered extraction, CIDOC CRM modeling, ")
        f.write("and social network analysis.\n\n")
        
        f.write("## Input Data\n\n")
        f.write(f"- **Source**: Einstein biography from `einstein.md`\n")
        f.write(f"- **Text Length**: {len(einstein_text)} characters\n")
        f.write(f"- **Analysis Date**: {Path.cwd()}\n\n")
        
        f.write("## Extraction Results\n\n")
        f.write(f"- **Total Entities**: {len(extraction_result.entities)}\n")
        f.write(f"- **Total Relationships**: {len(extraction_result.relationships)}\n\n")
        
        f.write("### Entity Breakdown by Type\n")
        for class_code, count in entity_types.items():
            f.write(f"- **{class_code}**: {count} entities\n")
        f.write("\n")
        
        f.write("## Network Analysis\n\n")
        f.write(f"- **Nodes**: {graph.number_of_nodes()}\n")
        f.write(f"- **Edges**: {graph.number_of_edges()}\n")
        f.write(f"- **Density**: {graph.density():.3f}\n")
        f.write(f"- **Communities**: {len(communities)}\n")
        f.write(f"- **Average Clustering**: {network_stats.get('basic_metrics', {}).get('average_clustering', 'N/A')}\n")
        f.write(f"- **Transitivity**: {network_stats.get('basic_metrics', {}).get('transitivity', 'N/A')}\n\n")
        
        if centrality_measures.get("degree"):
            f.write("### Most Central Entities\n")
            degree_centrality = centrality_measures["degree"]
            top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
            for i, (node_id, centrality) in enumerate(top_nodes, 1):
                node_data = graph.nodes[node_id]
                label = node_data.get("label", node_id)
                class_code = node_data.get("class_code", "Unknown")
                f.write(f"{i}. **{label}** ({class_code}) - Centrality: {centrality:.3f}\n")
            f.write("\n")
        
        f.write("## Community Structure\n\n")
        if communities:
            f.write(f"Found {len(communities)} communities:\n")
            for i, community in enumerate(communities, 1):
                f.write(f"\n### Community {i} ({len(community)} entities)\n")
                for node_id in community[:5]:  # Show first 5 entities
                    node_data = graph.nodes[node_id]
                    label = node_data.get("label", node_id)
                    f.write(f"- {label}\n")
                if len(community) > 5:
                    f.write(f"- ... and {len(community) - 5} more\n")
        f.write("\n")
        
        f.write("## Output Files\n\n")
        f.write("### Markdown Reports\n")
        f.write(f"- Entity cards: `{markdown_dir}/entity_*.md`\n")
        f.write(f"- Summary table: `{table_file}`\n")
        f.write(f"- Narratives: `{markdown_dir}/narrative_*.md`\n\n")
        
        f.write("### Visualizations\n")
        f.write(f"- Network overview: `{plots_dir}/network_overview.png`\n")
        f.write(f"- Community structure: `{plots_dir}/community_structure.png`\n")
        f.write(f"- Degree centrality: `{plots_dir}/degree_centrality.png`\n")
        f.write(f"- Interactive network: `{interactive_file}`\n\n")
        
        f.write("### Data Exports\n")
        f.write(f"- Cypher script: `{cypher_file}`\n")
        f.write(f"- Analysis report: `{report_file}`\n\n")
        
        f.write("## Methodology\n\n")
        f.write("This analysis used the following workflow:\n\n")
        f.write("1. **AI Extraction**: PydanticAI-powered text analysis to identify entities and relationships\n")
        f.write("2. **CRM Modeling**: Conversion to CIDOC CRM entities with proper class codes\n")
        f.write("3. **Markdown Rendering**: Human-readable reports for analysis and review\n")
        f.write("4. **Network Construction**: NetworkX graph with entities as nodes\n")
        f.write("5. **Social Network Analysis**: Centrality measures and community detection\n")
        f.write("6. **Visualization**: Static and interactive network plots\n")
        f.write("7. **Export**: Cypher scripts for graph database persistence\n\n")
        
        f.write("## Key Insights\n\n")
        f.write("The analysis reveals the complex network of entities and relationships ")
        f.write("in Einstein's life story, highlighting:\n\n")
        f.write("- **Central Figures**: Key people in Einstein's life and work\n")
        f.write("- **Important Events**: Significant life events and achievements\n")
        f.write("- **Geographic Context**: Places associated with Einstein's life\n")
        f.write("- **Temporal Patterns**: Chronological relationships between events\n")
        f.write("- **Community Structure**: Clusters of related entities\n\n")
        
        f.write("This demonstrates COLLIE's capability to transform unstructured biographical ")
        f.write("text into structured, analyzable knowledge graphs that preserve the semantic ")
        f.write("richness of cultural heritage information.\n")
    
    print(f"✅ Created comprehensive report: {report_file}")
    
    # Final summary
    print("\n🎉 Einstein Biography Demo Complete!")
    print("=" * 60)
    print(f"📁 All outputs saved to: {output_dir.absolute()}")
    print("\n📊 Summary:")
    print(f"  - Extracted {len(extraction_result.entities)} entities")
    print(f"  - Created network with {graph.number_of_nodes()} nodes")
    print(f"  - Found {len(communities)} communities")
    print(f"  - Generated {len(list(markdown_dir.glob('*.md')))} markdown reports")
    print(f"  - Created {len(list(plots_dir.glob('*')))} visualizations")
    print("\n🔗 Next Steps:")
    print(f"  - View interactive network: {interactive_file}")
    print(f"  - Read analysis report: {report_file}")
    print(f"  - Import to Neo4j: {cypher_file}")


async def main():
    """Main function."""
    if not check_requirements():
        sys.exit(1)
    
    try:
        await einstein_complete_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
