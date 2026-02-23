# CIDOC CRM Models

infoextract-cidoc provides Pydantic models for all CIDOC CRM v7.1.3 classes.

## Base Classes

### CRMEntity

```python
from infoextract_cidoc.models.base import CRMEntity

entity = CRMEntity(
    class_code="E21",
    label="Albert Einstein",
    notes="German-born theoretical physicist",
    type=["E21"]
)
```

### CRMRelation

```python
from infoextract_cidoc.models.base import CRMRelation

relation = CRMRelation(
    src=entity1.id,
    type="P98",  # was born
    tgt=entity2.id
)
```

## Generated E-Classes

All 99 E-classes are available:

```python
from infoextract_cidoc.models.generated.e_classes import E21_Person, E53_Place, E5_Event

person = E21_Person(label="Marie Curie")
place = E53_Place(label="Warsaw")
```

## Key Entity Types

| Class | Description | Common Properties |
|-------|-------------|-------------------|
| E21 Person | Human individual | P98 born, P100 died, P14 carried out |
| E5 Event | Historical event | P7 took place at, P11 participant |
| E53 Place | Geographic location | P87 identified by, P89 falls within |
| E22 Object | Human-made object | P108 produced by, P45 consists of |
| E52 Time-Span | Temporal extent | P82 at some time within |
