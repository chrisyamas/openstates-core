import pytest
from openstates.data.models import Jurisdiction, Division, Organization
from openstates.cli.initdb import create_division, create_chamber
from openstates_metadata import lookup
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_create_division_basic():
    div = create_division("ocd-division/country:us/state:nc", "North Carolina")
    assert div.name == "North Carolina"
    assert Division.objects.count() == 1


@pytest.mark.django_db
def test_create_division_duplicate():
    div = create_division("ocd-division/country:us/state:nc", "North Carolina")
    # first name persists b/c of get_or_create
    div = create_division("ocd-division/country:us/state:nc", "N. Carolina")
    assert div.name == "North Carolina"
    assert Division.objects.count() == 1


@pytest.mark.django_db
def test_create_chamber_basic():
    nc = lookup(abbr="NC")

    juris = Jurisdiction.objects.create(
        id=nc.jurisdiction_id, name=nc.name, division=None
    )
    leg = Organization.objects.create(
        id=nc.legislature_organization_id,
        name=nc.legislature_name,
        classification="legislature",
        jurisdiction=juris,
    )
    create_chamber(juris, leg, nc.lower)

    # ensure the org and posts were created
    org = Organization.objects.get(classification="lower")
    assert org.name == nc.lower.name
    assert org.id == nc.lower.organization_id
    assert org.posts.count() == 120


@pytest.mark.django_db
def test_create_chamber_duplicate_idempotent():
    nc = lookup(abbr="NC")

    juris = Jurisdiction.objects.create(
        id=nc.jurisdiction_id, name=nc.name, division=None
    )
    leg = Organization.objects.create(
        id=nc.legislature_organization_id,
        name=nc.legislature_name,
        classification="legislature",
        jurisdiction=juris,
    )

    # second call, identical to first, should be idempotent
    create_chamber(juris, leg, nc.lower)
    create_chamber(juris, leg, nc.lower)

    assert Organization.objects.filter(classification="lower").count() == 1

    # ensure the org and posts were created
    org = Organization.objects.get(classification="lower")
    assert org.name == nc.lower.name
    assert org.id == nc.lower.organization_id
    assert org.posts.count() == 120


@pytest.mark.django_db
def test_create_chamber_duplicate_with_changes():
    nc = lookup(abbr="NC")

    juris = Jurisdiction.objects.create(
        id=nc.jurisdiction_id, name=nc.name, division=None
    )
    leg = Organization.objects.create(
        id=nc.legislature_organization_id,
        name=nc.legislature_name,
        classification="legislature",
        jurisdiction=juris,
    )

    create_chamber(juris, leg, nc.lower)
    # second call, but lower chamber name has been changed
    nc.lower.name = "Ronald McDonald House of Clowns"
    with pytest.raises(IntegrityError):
        create_chamber(juris, leg, nc.lower)  # unsupported, should definitely be loud

    assert Organization.objects.filter(classification="lower").count() == 1
