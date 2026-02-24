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
from infoextract_cidoc.models.base import CRMEntity
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
        for _key in api_keys[:3]:
            pass
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

    # Step 1: LangStruct extraction + resolution + CRM mapping

    _lite_result, extraction_result, crm_entities, crm_relations = await _run_extraction(
        text
    )

    # Apply confidence threshold filter
    crm_entities = [
        e
        for e in crm_entities
        if not hasattr(e, "confidence") or True  # CRMEntity doesn't have confidence
    ]
    # Filter at the extraction_result level
    [
        e for e in extraction_result.entities if e.confidence >= confidence_threshold
    ]


    # Step 2: Serialize as Canonical JSON

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    json_data = [entity.model_dump(mode="json") for entity in crm_entities]
    json_file = output_path / "canonical_entities.json"
    with json_file.open("w") as f:
        json.dump(json_data, f, indent=2)


    # Step 3: Render to Markdown

    markdown_dir = output_path / "markdown"
    markdown_dir.mkdir(exist_ok=True)

    for i, entity in enumerate(crm_entities[:5]):
        markdown_card = to_markdown(entity, MarkdownStyle.CARD)
        card_file = markdown_dir / f"entity_{i + 1}_{entity.class_code}.md"
        with card_file.open("w") as f:
            f.write(markdown_card)

    table_markdown = render_table(crm_entities)
    table_file = markdown_dir / "entities_summary.md"
    with table_file.open("w") as f:
        f.write("# CRM Entities Summary\n\n" + table_markdown)


    # Step 4: Convert to NetworkX Graph

    graph = to_networkx_graph(crm_entities)

    # Step 5: Network Analysis

    calculate_centrality_measures(graph)
    communities = find_communities(graph)
    network_stats = create_network_summary(graph)


    # Step 6: Visualization
    if visualize or interactive:

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

    # Step 7: Export to Cypher
    if export_cypher:

        cypher_script = generate_cypher_script(crm_entities)
        cypher_file = output_path / "network.cypher"
        with cypher_file.open("w") as f:
            f.write(cypher_script)


    # Step 8: Create Summary Report

    summary_file = output_path / "workflow_summary.md"
    with summary_file.open("w") as f:
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




async def einstein_demo() -> None:
    """Run the Einstein biography demo."""

    einstein_file = Path("src/infoextract_cidoc/examples/einstein.md")
    if not einstein_file.exists():
        return

    with einstein_file.open() as f:
        einstein_text = f.read()

    await complete_workflow_demo(einstein_text, "einstein_output")


async def handle_extract_command(args: argparse.Namespace) -> None:
    """Handle the extract command."""
    if not args.text and not args.file:
        return

    if args.text and args.file:
        return

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            return
        with file_path.open() as f:
            text = f.read()
    else:
        text = args.text


    _lite_result, extraction_result, crm_entities, _crm_relations = await _run_extraction(
        text
    )

    # Apply confidence filter
    filtered_entities = [
        e for e in extraction_result.entities if e.confidence >= args.confidence
    ]
    filtered_relationships = [
        r for r in extraction_result.relationships if r.confidence >= args.confidence
    ]


    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    if args.format in ["json", "both"]:
        result_data = {
            "entities": [e.model_dump() for e in filtered_entities],
            "relationships": [r.model_dump() for r in filtered_relationships],
        }
        with (output_dir / "extraction_result.json").open("w") as f:
            json.dump(result_data, f, indent=2)

        canonical_json = [entity.model_dump(mode="json") for entity in crm_entities]
        with (output_dir / "canonical_entities.json").open("w") as f:
            json.dump(canonical_json, f, indent=2)

    if args.format in ["markdown", "both"]:
        markdown_content = render_table(crm_entities)
        with (output_dir / "extraction_result.md").open("w") as f:
            f.write(markdown_content)


async def handle_analyze_command(args: argparse.Namespace) -> None:
    """Handle the analyze command."""
    input_file = Path(args.input)
    if not input_file.exists():
        return


    with input_file.open() as f:
        data = json.load(f)

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
        return


    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    graph = to_networkx_graph(entities)

    if args.centrality:
        centrality_measures = calculate_centrality_measures(graph)
        with (output_dir / "centrality_measures.json").open("w") as f:
            json.dump(centrality_measures, f, indent=2)

    if args.communities:
        communities = find_communities(graph)
        community_data = {
            "num_communities": len(communities),
            "communities": [list(community) for community in communities],
        }
        with (output_dir / "communities.json").open("w") as f:
            json.dump(community_data, f, indent=2)

    if args.visualize:
        plot_network_graph(
            graph,
            title="CRM Entity Network",
            save_path=str(output_dir / "network_plot.png"),
            show_plot=False,
        )

    if args.export_cypher:
        cypher_script = generate_cypher_script(entities)
        with (output_dir / "entities.cypher").open("w") as f:
            f.write(cypher_script)


async def handle_workflow_command(args: argparse.Namespace) -> None:
    """Handle the workflow command."""
    if not args.text and not args.file:
        return

    if args.text and args.file:
        return

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            return
        with file_path.open() as f:
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
        pass


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
