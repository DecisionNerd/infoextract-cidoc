"""Shared test fixtures for infoextract-cidoc tests."""

from uuid import uuid4

import pytest

from infoextract_cidoc.models.base import CRMEntity, CRMRelation
from infoextract_cidoc.models.generated.e_classes import (
    E5_Event,
    E12_Production,
    E21_Person,
    E22_HumanMadeObject,
    E52_TimeSpan,
    E53_Place,
)


@pytest.fixture
def person_entity() -> E21_Person:
    return E21_Person(id=uuid4(), class_code="E21", label="Albert Einstein")


@pytest.fixture
def place_entity() -> E53_Place:
    return E53_Place(id=uuid4(), class_code="E53", label="Princeton")


@pytest.fixture
def event_entity(place_entity: E53_Place, timespan_entity: "E52_TimeSpan") -> E5_Event:
    return E5_Event(
        id=uuid4(),
        class_code="E5",
        label="Nobel Prize",
        timespan=timespan_entity.id,
        took_place_at=place_entity.id,
    )


@pytest.fixture
def timespan_entity() -> E52_TimeSpan:
    return E52_TimeSpan(id=uuid4(), class_code="E52", label="1921")


@pytest.fixture
def object_entity(
    place_entity: E53_Place, production_entity: E12_Production
) -> E22_HumanMadeObject:
    return E22_HumanMadeObject(
        id=uuid4(),
        class_code="E22",
        label="Ancient Vase",
        current_location=place_entity.id,
        produced_by=production_entity.id,
    )


@pytest.fixture
def production_entity(
    timespan_entity: E52_TimeSpan, place_entity: E53_Place
) -> E12_Production:
    return E12_Production(
        id=uuid4(),
        class_code="E12",
        label="Vase Production",
        timespan=timespan_entity.id,
        took_place_at=place_entity.id,
    )


@pytest.fixture
def sample_entities(
    person_entity: E21_Person,
    place_entity: E53_Place,
    event_entity: E5_Event,
) -> list[CRMEntity]:
    return [person_entity, place_entity, event_entity]


@pytest.fixture
def sample_relations(
    person_entity: E21_Person,
    place_entity: E53_Place,
) -> list[CRMRelation]:
    return [
        CRMRelation(src=person_entity.id, type="P74", tgt=place_entity.id),
    ]
