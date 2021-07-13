import typing
import uuid
from collections import defaultdict
import us  # type: ignore
import requests
import click
from ..models.people import (
    Person,
    OtherIdentifier,
    Role,
    Party,
    ContactDetail,
    Link,
    PersonIdBlock,
)  # type: ignore
from ..models.committees import Committee, Membership, ScrapeCommittee
from ..utils.people import dump_obj, get_data_path

# chosen at random, but needs to be constant
US_UUID_NAMESPACE = uuid.UUID("bf6b57c6-8cfe-454c-bd26-9c2b508c30b2")


def make_person_id(bioguide: str) -> str:
    return "ocd-person/" + str(uuid.uuid5(US_UUID_NAMESPACE, bioguide))


def get_district_offices() -> defaultdict[str, list[ContactDetail]]:
    district_offices = defaultdict(list)
    url = "https://theunitedstates.io/congress-legislators/legislators-district-offices.json"
    entries = requests.get(url).json()
    for entry in entries:
        for office in entry["offices"]:
            address = office.get("address", "")
            if address:
                if office.get("suite"):
                    address += " " + office["suite"]
                address += f"; {office['city']}, {office['state']} {office['zip']}"

            district_offices[entry["id"]["bioguide"]].append(
                ContactDetail(
                    note="District Office",
                    voice=office.get("phone", ""),
                    fax=office.get("fax", ""),
                    address=address,
                )
            )
    return district_offices


def get_social() -> dict[str, PersonIdBlock]:
    social: dict[str, PersonIdBlock] = {}
    url = (
        "https://theunitedstates.io/congress-legislators/legislators-social-media.json"
    )
    entries = requests.get(url).json()
    for entry in entries:
        social[entry["id"]["bioguide"]] = PersonIdBlock(
            twitter=entry["social"].get("twitter", ""),
            facebook=entry["social"].get("facebook", ""),
            youtube=entry["social"].get("youtube_id", ""),
        )
    return social


def fetch_current_people() -> typing.Iterable[tuple[str, Person]]:
    url = "https://theunitedstates.io/congress-legislators/legislators-current.json"
    legislators = requests.get(url).json()
    for leg in legislators:
        yield current_to_person(leg)


def current_to_person(current: dict[str, typing.Any]) -> tuple[str, Person]:
    full_name = current["name"].get(
        "official_full", f"{current['name']['first']} {current['name']['last']}"
    )
    bioguide = current["id"]["bioguide"]
    p = Person(
        id=make_person_id(bioguide),
        name=full_name,
        given_name=current["name"]["first"],
        family_name=current["name"]["last"],
        middle_name=current["name"].get("middle", ""),
        gender=current["bio"]["gender"],
        birth_date=current["bio"]["birthday"],
        roles=[],
    )
    for key, value in current["id"].items():
        if isinstance(value, list):
            for identifier in value:
                p.other_identifiers.append(
                    OtherIdentifier(scheme=key, identifier=identifier)
                )
        else:
            p.other_identifiers.append(OtherIdentifier(scheme=key, identifier=value))

    # keep mapping of start & end dates of party memberships
    parties: dict[str, dict[str, str]] = defaultdict(dict)
    for term in current["terms"]:
        if term["start"] < parties[term["party"]].get("start", "9999-99-99"):
            parties[term["party"]]["start"] = term["start"]
        if term["end"] > parties[term["party"]].get("end", ""):
            parties[term["party"]]["end"] = term["end"]
        if term["type"] == "sen":
            role_type = "upper"
            district = us.states.lookup(term["state"]).name
            # division_id = f"ocd-division/country:us/state:{term['state']}"
        elif term["type"] == "rep":
            role_type = "lower"
            if term["district"] == 0:
                district = f"{term['state']}-AL"
            else:
                district = f"{term['state']}-{term['district']}"
            # division_id = f"ocd-division/country:us/state:{term['state']}/cd:{term['district']}"
        role = Role(
            type=role_type,
            district=district,
            jurisdiction="ocd-jurisdiction/country:us/government",
            start_date=term["start"],
            end_date=term["end"],
        )
        p.roles.append(role)

    # add party memberships
    for name, times in parties.items():
        if name == "Democrat":
            name = "Democratic"
        p.party.append(
            Party(name=name, start_date=times["start"], end_date=times["end"])
        )

    # add contact info from latest term
    cur_term = current["terms"][-1]
    if "url" in cur_term:
        p.links.append(Link(note="website", url=cur_term["url"]))
    if "contact_form" in cur_term:
        p.links.append(Link(note="contact form", url=cur_term["contact_form"]))

    p.contact_details.append(
        ContactDetail(
            note="Capitol Office",
            address=cur_term.get("address", ""),
            voice=cur_term.get("phone", ""),
        )
    )

    return bioguide, p


def scrape_people() -> None:
    output_dir = get_data_path("us") / "legislature"
    district_offices = get_district_offices()
    social = get_social()
    for bioguide, person in fetch_current_people():
        person.contact_details.extend(district_offices[bioguide])
        if bioguide in social:
            person.ids = social[bioguide]
        person.sources.append(Link(url="https://theunitedstates.io/"))
        person.image = (
            f"https://theunitedstates.io/images/congress/450x550/{bioguide}.jpg"
        )
        dump_obj(person, output_dir=output_dir)


def get_thomas_mapping(convert_chamber: dict) -> dict[tuple[str, str, str], list[str]]:
    """
    This function creates a dictionary that maps a tuple to a list of thomas_ids.
    This tuple differs depending on if its mapping a committee versus a subcommittee.
    Committee tuples consist of (chamber, name, type).
    Subcommittee tuples consiste of (name, sub_name, type).
    """
    name_mapping: dict[tuple[str, str, str], list[str]] = {}
    url = "https://theunitedstates.io/congress-legislators/committees-current.json"
    committees = requests.get(url).json()

    for com in committees:
        name = com["name"]
        thomas_id = com["thomas_id"]
        type = com["type"]
        chamber = convert_chamber[type]

        name_mapping[(chamber, name, type)] = name_mapping.get(
            (chamber, name, type), []
        ) + [thomas_id]

        if "subcommittees" in com:
            for sub in com["subcommittees"]:
                sub_name = sub["name"]
                thomas_id_agg = thomas_id + sub["thomas_id"]
                name_mapping[(name, sub_name, type)] = name_mapping.get(
                    (name, sub_name, type), []
                ) + [thomas_id_agg]

    return name_mapping


def fetch_current_committees(convert_chamber: dict) -> typing.Iterable[Committee]:
    url = "https://theunitedstates.io/congress-legislators/committees-current.json"
    committees = requests.get(url).json()
    for com in committees:
        committee_name = com["name"]
        thomas_id = com["thomas_id"]
        chamber = convert_chamber[com["type"]]

        c = Committee(
            id="ocd-organization/" + str(uuid.uuid5(US_UUID_NAMESPACE, thomas_id)),
            jurisdiction="ocd-jurisdiction/country:us/government",
            name=committee_name,
            parent=chamber,
        )

        if "address" in com:
            c.extras["address"] = com["address"]
        if "phone" in com:
            c.extras["phone"] = com["phone"]
        if "url" in com:
            c.add_link(com["url"], note="homepage")
        if "minority_url" in com:
            c.add_link(com["minority_url"], note="homepage")

        c.extras["type"] = com["type"]

        yield c

        if "subcommittees" in com:
            for sub in com["subcommittees"]:
                subcommittee_name = sub["name"]
                sub_thomas_id = sub["thomas_id"]
                sub_thomas_id = thomas_id + sub_thomas_id
                s = Committee(
                    id="ocd-organization/"
                    + str(uuid.uuid5(US_UUID_NAMESPACE, sub_thomas_id)),
                    jurisdiction="ocd-jurisdiction/country:us/government",
                    name=subcommittee_name,
                    parent=committee_name,
                    classification="subcommittee",
                )

                if "address" in sub:
                    s.extras["address"] = sub["address"]
                if "phone" in sub:
                    s.extras["phone"] = sub["phone"]

                s.extras["type"] = com["type"]

                yield s


def get_members_mapping() -> dict[str, list]:
    url = "https://theunitedstates.io/congress-legislators/committee-membership-current.json"
    members_mapping = requests.get(url).json()

    return members_mapping


def grab_members(
    committee: ScrapeCommittee,
    name_mapping: list[str],
    members_mapping: dict[str, list],
) -> None:
    for t_id in name_mapping:
        if t_id in members_mapping:
            members = members_mapping[t_id]
            for member in members:
                if "title" in member:
                    committee.members.append(
                        Membership(
                            name=member["name"],
                            role=member["title"],
                            person_id=make_person_id(member["bioguide"]),
                        )
                    )
                else:
                    committee.members.append(
                        Membership(
                            name=member["name"],
                            role="Member",
                            person_id=make_person_id(member["bioguide"]),
                        )
                    )


def scrape_committees() -> None:
    output_dir = get_data_path("us") / "committees"

    convert_chamber = {"house": "lower", "senate": "upper", "joint": "legislature"}

    members_mapping = get_members_mapping()
    name_mapping = get_thomas_mapping(convert_chamber)

    for committee in fetch_current_committees(convert_chamber):
        name = committee.name
        chamber = committee.extras["type"]

        grab_members(
            committee, name_mapping[(committee.parent, name, chamber)], members_mapping
        )
        committee.sources.append(Link(url="https://theunitedstates.io/"))

        if len(committee.members) > 0:
            dump_obj(committee, output_dir=output_dir)


@click.command()
def main() -> None:
    """
    Create/Update United States legislators from unitedstates.io
    """
    scrape_people()
    scrape_committees()


if __name__ == "__main__":
    main()