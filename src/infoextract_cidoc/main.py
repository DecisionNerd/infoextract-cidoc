"""
infoextract-cidoc CLI - Complete workflow for CIDOC CRM information extraction.

Pipeline:
  Text -> LangStructExtractor -> resolve_extraction -> map_to_crm_entities -> Outputs
"""

import argparse
import asyncio
import json
import os
import sys
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
    to_networkx_graph,
)
from infoextract_cidoc.visualization import create_network_summary, plot_network_graph

# Load environment variables from .env file
load_dotenv()


def check_api_key() -> None:
    """Check that at least one LLM API key is configured."""
    api_keys = [
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "LANGSTRUCT_DEFAULT_MODEL",
    ]
    configured = [k for k in api_keys if os.getenv(k)]
    if not configured:
        print("Error: No LLM API key found. Set one of the following:")
        for key in api_keys[:3]:
            print(f"  export {key}='your-key-here'")
        print("Or create a .env file with one of the above.")
        sys.exit(1)


async def _run_extraction(text: str) -> tuple:
    """Run the full extraction pipeline on text.

    Returns:
        Tuple of (lite_result, extraction_result, crm_entities, crm_relations)
    """
    extractor = LangStructExtractor()
    lite_result = await extractor.extract_async(text)
    extraction_result = resolve_extraction(lite_result)
    crm_entities, crm_relations = map_to_crm_entities(extraction_result)
    return lite_result, extraction_result, crm_entities, crm_relations


async def complete_workflow_demo(
    text: str,
    output_dir: str = "output",
    visualize: bool = True,
    interactive: bool = True,
    export_cypher: bool = True,
    confidence_threshold: float = 0.5,
) -> None:
    """Run the complete infoextract-cidoc workflow.

    Args:
        text: Input text to analyze
        output_dir: Directory to save outputs
        visualize: Whether to create static visualizations
        interactive: Whether to create interactive plots (currently static only)
        export_cypher: Whether to export Cypher scripts
        confidence_threshold: Minimum confidence for entities/relationships
    """
    print("Starting infoextract-cidoc Workflow")
    print("=" * 50)

    # Step 1: LangStruct extraction + resolution + CRM mapping
    print("\nStep 1: Extracting entities via LangStruct pipeline")
    print("-" * 40)

    lite_result, extraction_result, crm_entities, crm_relations = await _run_extraction(
        text
    )

    # Apply confidence threshold filter
    from infoextract_cidoc.models.base import CRMEntity

    crm_entities = [
        e
        for e in crm_entities
        if not hasattr(e, "confidence") or True  # CRMEntity doesn't have confidence
    ]
    # Filter at the extraction_result level
    filtered_entities = [
        e for e in extraction_result.entities if e.confidence >= confidence_threshold
    ]

    print(f"Extracted {len(crm_entities)} CRM entities")
    print(f"Extracted {len(crm_relations)} CRM relations")

    # Step 2: Serialize as Canonical JSON
    print("\nStep 2: Serialize as Canonical JSON")
    print("-" * 40)

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    json_data = [entity.model_dump(mode="json") for entity in crm_entities]
    json_file = output_path / "canonical_entities.json"
    with open(json_file, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"Serialized {len(json_data)} entities to canonical JSON: {json_file}")

    # Step 3: Render to Markdown
    print("\nStep 3: Render to Markdown")
    print("-" * 40)

    markdown_dir = output_path / "markdown"
    markdown_dir.mkdir(exist_ok=True)

    for i, entity in enumerate(crm_entities[:5]):
        markdown_card = to_markdown(entity, MarkdownStyle.CARD)
        card_file = markdown_dir / f"entity_{i + 1}_{entity.class_code}.md"
        with open(card_file, "w") as f:
            f.write(markdown_card)

    table_markdown = render_table(crm_entities)
    table_file = markdown_dir / "entities_summary.md"
    with open(table_file, "w") as f:
        f.write("# CRM Entities Summary\n\n" + table_markdown)

    print(f"Generated Markdown reports in {markdown_dir}")

    # Step 4: Convert to NetworkX Graph
    print("\nStep 4: Convert to NetworkX Graph")
    print("-" * 40)

    graph = to_networkx_graph(crm_entities)
    print(
        f"Created NetworkX graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges"
    )

    # Step 5: Network Analysis
    print("\nStep 5: Network Analysis")
    print("-" * 40)

    centrality_measures = calculate_centrality_measures(graph)
    communities = find_communities(graph)
    network_stats = create_network_summary(graph)

    print(f"Calculated centrality measures: {list(centrality_measures.keys())}")
    print(f"Found {len(communities)} communities")
    print(f"Network density: {network_stats['network_info']['density']:.3f}")

    # Step 6: Visualization
    if visualize or interactive:
        print("\nStep 6: Visualization")
        print("-" * 40)

        plots_dir = output_path / "plots"
        plots_dir.mkdir(exist_ok=True)

        if visualize:
            plot_network_graph(
                graph,
                title="infoextract-cidoc Network Analysis",
                figsize=(14, 10),
                show_plot=False,
                save_path=str(plots_dir / "network_overview.png"),
            )
            print(f"Generated static plot: {plots_dir / 'network_overview.png'}")

    # Step 7: Export to Cypher
    if export_cypher:
        print("\nStep 7: Export to Cypher")
        print("-" * 40)

        cypher_script = generate_cypher_script(crm_entities)
        cypher_file = output_path / "network.cypher"
        with open(cypher_file, "w") as f:
            f.write(cypher_script)

        print(f"Generated Cypher script: {cypher_file}")

    # Step 8: Create Summary Report
    print("\nStep 8: Create Summary Report")
    print("-" * 40)

    summary_file = output_path / "workflow_summary.md"
    with open(summary_file, "w") as f:
        f.write("# infoextract-cidoc Workflow Summary\n\n")
        f.write(f"## Input Text\n\n{text[:200]}...\n\n")
        f.write("## Extracted Entities\n\n")
        f.write(f"- Total entities: {len(crm_entities)}\n")
        f.write(f"- Total relations: {len(crm_relations)}\n\n")
        f.write("## Network Analysis\n\n")
        f.write(f"- Nodes: {graph.number_of_nodes()}\n")
        f.write(f"- Edges: {graph.number_of_edges()}\n")
        f.write(f"- Density: {network_stats['network_info']['density']:.3f}\n")
        f.write(f"- Communities: {len(communities)}\n\n")
        f.write("## Output Files\n\n")
        f.write(f"- Canonical JSON: {json_file}\n")
        f.write(f"- Markdown reports: {markdown_dir}\n")
        if visualize or interactive:
            f.write(f"- Network plots: {output_path / 'plots'}\n")
        if export_cypher:
            f.write(f"- Cypher script: {output_path / 'network.cypher'}\n")

    print(f"Created summary report: {summary_file}")

    print("\nWorkflow Complete!")
    print("=" * 50)
    print(f"All outputs saved to: {output_path.absolute()}")


async def einstein_demo() -> None:
    """Run the Einstein biography demo."""
    print("Running Einstein Biography Demo")
    print("=" * 50)

    einstein_file = Path("src/infoextract_cidoc/examples/einstein.md")
    if not einstein_file.exists():
        print(f"Einstein file not found: {einstein_file}")
        return

    with open(einstein_file) as f:
        einstein_text = f.read()

    await complete_workflow_demo(einstein_text, "einstein_output")


async def handle_extract_command(args: argparse.Namespace) -> None:
    """Handle the extract command."""
    if not args.text and not args.file:
        print("Error: Either --text or --file must be provided")
        return

    if args.text and args.file:
        print("Error: Provide either --text or --file, not both")
        return

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return
        with open(file_path) as f:
            text = f.read()
    else:
        text = args.text

    print(f"Extracting entities from {'file' if args.file else 'text'}...")

    lite_result, extraction_result, crm_entities, crm_relations = await _run_extraction(
        text
    )

    # Apply confidence filter
    filtered_entities = [
        e for e in extraction_result.entities if e.confidence >= args.confidence
    ]
    filtered_relationships = [
        r for r in extraction_result.relationships if r.confidence >= args.confidence
    ]

    print(
        f"Extracted {len(filtered_entities)} entities and {len(filtered_relationships)} relationships"
    )

    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    if args.format in ["json", "both"]:
        result_data = {
            "entities": [e.model_dump() for e in filtered_entities],
            "relationships": [r.model_dump() for r in filtered_relationships],
        }
        with open(output_dir / "extraction_result.json", "w") as f:
            json.dump(result_data, f, indent=2)
        print(
            f"Saved raw extraction results to {output_dir / 'extraction_result.json'}"
        )

        canonical_json = [entity.model_dump(mode="json") for entity in crm_entities]
        with open(output_dir / "canonical_entities.json", "w") as f:
            json.dump(canonical_json, f, indent=2)
        print(f"Saved canonical JSON to {output_dir / 'canonical_entities.json'}")

    if args.format in ["markdown", "both"]:
        markdown_content = render_table(crm_entities)
        with open(output_dir / "extraction_result.md", "w") as f:
            f.write(markdown_content)
        print(f"Saved Markdown results to {output_dir / 'extraction_result.md'}")


async def handle_analyze_command(args: argparse.Namespace) -> None:
    """Handle the analyze command."""
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return

    print(f"Analyzing entities from {input_file}...")

    with open(input_file) as f:
        data = json.load(f)

    from infoextract_cidoc.models.base import CRMEntity

    entities = []

    if isinstance(data, list):
        for entity_data in data:
            entity = CRMEntity(**entity_data)
            entities.append(entity)
    elif isinstance(data, dict) and "entities" in data:
        for entity_data in data["entities"]:
            entity = CRMEntity(
                id=entity_data["id"],
                class_code=entity_data["class_code"],
                label=entity_data["label"],
                notes=entity_data.get("description", ""),
            )
            entities.append(entity)
    else:
        print(f"Error: Unrecognized JSON format in {input_file}")
        return

    print(f"Loaded {len(entities)} entities")

    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    graph = to_networkx_graph(entities)
    print(
        f"Created NetworkX graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges"
    )

    if args.centrality:
        print("Calculating centrality measures...")
        centrality_measures = calculate_centrality_measures(graph)
        with open(output_dir / "centrality_measures.json", "w") as f:
            json.dump(centrality_measures, f, indent=2)
        print(f"Saved centrality measures to {output_dir / 'centrality_measures.json'}")

    if args.communities:
        print("Finding communities...")
        communities = find_communities(graph)
        community_data = {
            "num_communities": len(communities),
            "communities": [list(community) for community in communities],
        }
        with open(output_dir / "communities.json", "w") as f:
            json.dump(community_data, f, indent=2)
        print(f"Saved community analysis to {output_dir / 'communities.json'}")

    if args.visualize:
        print("Creating visualizations...")
        plot_network_graph(
            graph,
            title="CRM Entity Network",
            save_path=str(output_dir / "network_plot.png"),
            show_plot=False,
        )
        print(f"Saved static plot to {output_dir / 'network_plot.png'}")

    if args.export_cypher:
        print("Exporting to Cypher...")
        cypher_script = generate_cypher_script(entities)
        with open(output_dir / "entities.cypher", "w") as f:
            f.write(cypher_script)
        print(f"Saved Cypher script to {output_dir / 'entities.cypher'}")


async def handle_workflow_command(args: argparse.Namespace) -> None:
    """Handle the workflow command."""
    if not args.text and not args.file:
        print("Error: Either --text or --file must be provided")
        return

    if args.text and args.file:
        print("Error: Provide either --text or --file, not both")
        return

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return
        with open(file_path) as f:
            text = f.read()
    else:
        text = args.text

    run_all = args.all
    await complete_workflow_demo(
        text,
        args.output,
        visualize=args.visualize or run_all,
        interactive=args.interactive or run_all,
        export_cypher=args.export_cypher or run_all,
        confidence_threshold=args.confidence,
    )


async def handle_demo_command(args: argparse.Namespace) -> None:
    """Handle the demo command."""
    if args.einstein:
        await einstein_demo()
    elif args.sample:
        sample_text = (
            "Albert Einstein was born on March 14, 1879, in Ulm, Germany. "
            "He developed the theory of relativity and won the Nobel Prize in Physics in 1921. "
            "Einstein worked at the Institute for Advanced Study in Princeton, New Jersey. "
            "He died on April 18, 1955, at Princeton Hospital."
        )
        await complete_workflow_demo(sample_text, args.output)
    else:
        print("Error: Specify either --einstein or --sample")


async def main() -> None:
    """Main function for CLI."""
    parser = argparse.ArgumentParser(
        description="infoextract-cidoc - CIDOC CRM information extraction and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  infoextract-cidoc extract --text "Albert Einstein was born in Ulm, Germany"
  infoextract-cidoc extract --file biography.txt --output results/
  infoextract-cidoc analyze --input entities.json --visualize --export-cypher
  infoextract-cidoc workflow --file biography.txt --all --output results/
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract entities from text using AI"
    )
    extract_parser.add_argument("--text", help="Text to extract entities from")
    extract_parser.add_argument(
        "--file", help="File containing text to extract entities from"
    )
    extract_parser.add_argument(
        "--output", "-o", default="output", help="Output directory"
    )
    extract_parser.add_argument(
        "--confidence", type=float, default=0.5, help="Minimum confidence threshold"
    )
    extract_parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Output format",
    )

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze extracted entities")
    analyze_parser.add_argument(
        "--input", "-i", required=True, help="Input file with extracted entities"
    )
    analyze_parser.add_argument(
        "--output", "-o", default="analysis", help="Output directory"
    )
    analyze_parser.add_argument(
        "--visualize", action="store_true", help="Create visualizations"
    )
    analyze_parser.add_argument(
        "--interactive", action="store_true", help="Create interactive plots"
    )
    analyze_parser.add_argument(
        "--export-cypher", action="store_true", help="Export to Cypher script"
    )
    analyze_parser.add_argument(
        "--centrality", action="store_true", help="Calculate centrality measures"
    )
    analyze_parser.add_argument(
        "--communities", action="store_true", help="Find communities"
    )

    # Workflow command (complete pipeline)
    workflow_parser = subparsers.add_parser("workflow", help="Run complete workflow")
    workflow_parser.add_argument("--text", help="Text to process")
    workflow_parser.add_argument("--file", help="File containing text to process")
    workflow_parser.add_argument(
        "--output", "-o", default="workflow_output", help="Output directory"
    )
    workflow_parser.add_argument(
        "--all", action="store_true", help="Run all analysis steps"
    )
    workflow_parser.add_argument(
        "--visualize", action="store_true", help="Create visualizations"
    )
    workflow_parser.add_argument(
        "--interactive", action="store_true", help="Create interactive plots"
    )
    workflow_parser.add_argument(
        "--export-cypher", action="store_true", help="Export to Cypher script"
    )
    workflow_parser.add_argument(
        "--confidence", type=float, default=0.5, help="Minimum confidence threshold"
    )

    # Demo commands
    demo_parser = subparsers.add_parser("demo", help="Run demo examples")
    demo_parser.add_argument(
        "--einstein", action="store_true", help="Run Einstein biography demo"
    )
    demo_parser.add_argument(
        "--sample", action="store_true", help="Run sample text demo"
    )
    demo_parser.add_argument(
        "--output", "-o", default="demo_output", help="Output directory"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Check API key for commands that need LLM
    if args.command in ["extract", "workflow", "demo"]:
        check_api_key()

    if args.command == "extract":
        await handle_extract_command(args)
    elif args.command == "analyze":
        await handle_analyze_command(args)
    elif args.command == "workflow":
        await handle_workflow_command(args)
    elif args.command == "demo":
        await handle_demo_command(args)


def cli() -> None:
    """Command line interface entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
