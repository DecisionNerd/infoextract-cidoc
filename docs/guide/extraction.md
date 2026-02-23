# Extraction Pipeline

infoextract-cidoc uses a three-stage extraction pipeline:

## Stage 1: LangStruct Extraction

`LangStructExtractor` wraps LangStruct with the `LiteExtractionResult` schema to extract entities and relationships in a single LLM call.

```python
from infoextract_cidoc.extraction import LangStructExtractor

extractor = LangStructExtractor(model="gemini/gemini-2.5-flash")
lite_result = extractor.extract(text)
# lite_result.entities: list of LiteEntity
# lite_result.relationships: list of LiteRelationship
```

### LiteEntity Fields
- `ref_id`: Short identifier used in relationships (e.g., `"person_1"`)
- `entity_type`: One of `Person`, `Event`, `Place`, `Object`, `TimeSpan`
- `label`: Human-readable name
- `description`: Optional description
- `confidence`: Score from 0.0 to 1.0
- `source_snippet`: Relevant text from the source

### LiteRelationship Fields
- `source_ref`, `target_ref`: `ref_id` values referencing entities
- `property_code`: CIDOC CRM P-code (e.g., `"P98"`)
- `property_label`: Human-readable label (e.g., `"was born"`)
- `confidence`: Score from 0.0 to 1.0

## Stage 2: Entity Resolution

`resolve_extraction()` builds an entity registry and assigns stable UUIDs.

```python
from infoextract_cidoc.extraction import resolve_extraction

extraction_result = resolve_extraction(lite_result)
# extraction_result.entities: list of ExtractedEntity (with stable UUIDs)
# extraction_result.relationships: list of ExtractedRelationship (refs resolved)
```

- **Stable UUIDs**: Generated via `uuid5(NAMESPACE_DNS, ref_id + label)` for deterministic IDs
- **Deduplication**: Entities with the same label are merged
- **Broken Link Handling**: Relationships with unresolvable refs are logged and excluded

## Stage 3: CRM Mapping

`map_to_crm_entities()` maps extracted entities to CIDOC CRM classes.

```python
from infoextract_cidoc.extraction import map_to_crm_entities

crm_entities, crm_relations = map_to_crm_entities(extraction_result)
```

Entity type dispatch:
- `Person` -> `E21_Person`
- `Event` -> `E5_Event`
- `Place` -> `E53_Place`
- `Object` -> `E22_HumanMadeObject`
- `TimeSpan` -> `E52_TimeSpan`

## Async and Batch Extraction

```python
# Async (non-blocking)
lite_result = await extractor.extract_async(text)

# Batch processing
results = extractor.extract_batch([text1, text2, text3])
```

## Model Configuration

```python
# Default: reads LANGSTRUCT_DEFAULT_MODEL env var or gemini/gemini-2.5-flash
extractor = LangStructExtractor()

# Explicit model
extractor = LangStructExtractor(model="openai/gpt-4o-mini")
```
