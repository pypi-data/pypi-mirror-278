import base64
import csv
import json
import uuid

import pytest

from allspice import AllSpice
from allspice.utils.bom_generation import (
    generate_bom,
    generate_bom_for_altium,
    generate_bom_for_orcad,
)
from allspice.utils.list_components import list_components_for_altium, list_components_for_orcad
from allspice.utils.netlist_generation import generate_netlist

test_repo = "repo_" + uuid.uuid4().hex[:8]
test_branch = "branch_" + uuid.uuid4().hex[:8]


@pytest.fixture(scope="session")
def port(pytestconfig):
    """Load --port command-line arg if set"""
    return pytestconfig.getoption("port")


@pytest.fixture
def instance(port):
    try:
        g = AllSpice(
            f"http://localhost:{port}",
            open(".token", "r").read().strip(),
            ratelimiting=None,
        )
        print("AllSpice Hub Version: " + g.get_version())
        print("API-Token belongs to user: " + g.get_user().username)

        return g
    except Exception:
        assert False, f"AllSpice Hub could not load. Is there: \
                - an Instance running at http://localhost:{port} \
                - a Token at .token \
                    ?"


def _setup_for_generation(instance, test_name, clone_addr):
    # TODO: we should commit a smaller set of files in this repo so we don't depend on external data
    instance.requests_post(
        "/repos/migrate",
        data={
            "clone_addr": clone_addr,
            "mirror": False,
            "repo_name": "-".join([test_repo, test_name]),
            "service": "git",
        },
    )


def test_bom_generation_flat(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        # We hard-code a ref so that this test is reproducible.
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
    )

    assert len(bom) == 925

    with open("tests/data/archimajor_bom_flat_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_with_odd_line_endings(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    # We hard-code a ref so that this test is reproducible.
    ref = "95719adde8107958bf40467ee092c45b6ddaba00"
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }

    new_branch_name = "-".join([test_branch, request.node.name])
    repo.add_branch(ref, new_branch_name)
    ref = new_branch_name

    files_in_repo = repo.get_git_content(ref=ref)
    prjpcb_file = next((x for x in files_in_repo if x.path == "Archimajor.PrjPcb"), None)
    assert prjpcb_file is not None

    original_prjpcb_sha = prjpcb_file.sha
    prjpcb_content = repo.get_raw_file(prjpcb_file.path, ref=ref).decode("utf-8")
    new_prjpcb_content = prjpcb_content.replace("\r\n", "\n\r")
    new_content_econded = base64.b64encode(new_prjpcb_content.encode("utf-8")).decode("utf-8")
    repo.change_file(
        "Archimajor.PrjPcb",
        original_prjpcb_sha,
        new_content_econded,
        {"branch": ref},
    )

    # Sanity check that the file was changed.
    prjpcb_content_now = repo.get_raw_file("Archimajor.PrjPcb", ref=ref).decode("utf-8")
    assert prjpcb_content_now != prjpcb_content

    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        # Note that ref here is the branch, not a commit sha as in the previous
        # test.
        ref=ref,
    )

    assert len(bom) == 925

    with open("tests/data/archimajor_bom_flat_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_grouped(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }

    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        group_by=["part_number", "manufacturer", "description"],
        # We hard-code a ref so that this test is reproducible.
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
    )

    assert len(bom) == 108

    with open("tests/data/archimajor_bom_grouped_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_with_folder_hierarchy(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorInFolders.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        group_by=["part_number"],
        # We hard-code a ref so that this test is reproducible.
        ref="e39ecf4de0c191559f5f23478c840ac2b6676d58",
    )

    assert len(bom) == 102

    with open("tests/data/archimajor_bom_hierarchical_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_with_default_variant(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorVariants.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        ref="916e739f3ad9d956f4e2a293542050e1df9e6f9e",
        # For the variants tests, we don't want to remove non-BOM components
        # because some of them are enabled by the variants, and we want to
        # test that they are included when required.
        remove_non_bom_components=False,
    )

    # Since we haven't specified a variant, this should have the same result
    # as generating a flat BOM. This version of archimajor has a few parts
    # removed even before the variations, so the number of parts is different.
    assert len(bom) == 987

    with open("tests/data/archimajor_bom_default_flat_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_with_fitted_variant(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorVariants.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        ref="916e739f3ad9d956f4e2a293542050e1df9e6f9e",
        variant="Fitted",
        remove_non_bom_components=False,
    )

    # Exactly 42 rows should be removed, as that is the number of non-param
    # variations.
    assert len(bom) == 987 - 42

    with open("tests/data/archimajor_bom_fitted_flat_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_with_grouped_variant(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorVariants.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        group_by=["part_number"],
        ref="916e739f3ad9d956f4e2a293542050e1df9e6f9e",
        variant="Fitted",
        remove_non_bom_components=False,
    )

    assert len(bom) == 89

    with open("tests/data/archimajor_bom_fitted_grouped_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_altium_with_non_bom_components(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        attributes_mapping,
        # We hard-code a ref so that this test is reproducible.
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
        remove_non_bom_components=False,
    )

    assert len(bom) == 1061

    with open("tests/data/archimajor_bom_non_bom_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_bom_generation_orcad(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/beagleplay.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    attributes_mapping = {
        "Name": ["_name"],
        "Description": "Description",
        "Reference designator": ["Part Reference"],
        "Manufacturer": ["Manufacturer", "MANUFACTURER"],
        "Part Number": ["Manufacturer PN", "PN"],
    }

    bom = generate_bom_for_orcad(
        instance,
        repo,
        "Design/BEAGLEPLAYV10_221227.DSN",
        attributes_mapping,
        # We hard-code a ref so that this test is reproducible.
        ref="7a59a98ae27dc4fd9e2bd8975ff90cdb44a366ea",
    )

    assert len(bom) == 870

    with open("tests/data/beagleplay_bom_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_generate_bom(request, instance):
    # Test the one-stop API which should automatically figure out the project
    # type and call the appropriate function.
    _setup_for_generation(
        instance,
        request.node.name + "altium",
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    _setup_for_generation(
        instance,
        request.node.name + "orcad",
        "https://hub.allspice.io/AllSpiceMirrors/beagleplay.git",
    )

    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name + "altium"])
    )
    altium_attributes_mapping = {
        "description": ["PART DESCRIPTION"],
        "designator": ["Designator"],
        "manufacturer": ["Manufacturer", "MANUFACTURER"],
        "part_number": ["PART", "MANUFACTURER #"],
    }
    bom = generate_bom(
        instance,
        repo,
        "Archimajor.PrjPcb",
        altium_attributes_mapping,
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
    )
    assert len(bom) == 925
    with open("tests/data/archimajor_bom_flat_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row

    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name + "orcad"])
    )
    orcad_attributes_mapping = {
        "Name": ["_name"],
        "Description": "Description",
        "Reference designator": ["Part Reference"],
        "Manufacturer": ["Manufacturer", "MANUFACTURER"],
        "Part Number": ["Manufacturer PN", "PN"],
    }
    bom = generate_bom(
        instance,
        repo,
        "Design/BEAGLEPLAYV10_221227.DSN",
        orcad_attributes_mapping,
        ref="7a59a98ae27dc4fd9e2bd8975ff90cdb44a366ea",
    )
    assert len(bom) == 870
    with open("tests/data/beagleplay_bom_expected.csv", "r") as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, bom):
            assert row == expected_row


def test_orcad_components_list(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/beagleplay.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )

    components = list_components_for_orcad(
        instance,
        repo,
        "Design/BEAGLEPLAYV10_221227.DSN",
        # We hard-code a ref so that this test is reproducible.
        ref="7a59a98ae27dc4fd9e2bd8975ff90cdb44a366ea",
    )

    assert len(components) == 870

    with open("tests/data/beagleplay_components_expected.json", "r") as f:
        assert json.loads(f.read()) == components


def test_altium_components_list(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )

    components = list_components_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        # We hard-code a ref so that this test is reproducible.
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
    )

    assert len(components) == 1061

    with open("tests/data/archimajor_components_expected.json", "r") as f:
        assert json.loads(f.read()) == components


def test_altium_components_list_with_folder_hierarchy(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorInFolders.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )

    components = list_components_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        # We hard-code a ref so that this test is reproducible.
        ref="e39ecf4de0c191559f5f23478c840ac2b6676d58",
    )

    assert len(components) == 1049

    with open("tests/data/archimajor_components_hierarchical_expected.json", "r") as f:
        assert json.loads(f.read()) == components


def test_altium_components_list_with_fitted_variant(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/AllSpiceMirrors/ArchimajorVariants.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )

    components = list_components_for_altium(
        instance,
        repo,
        "Archimajor.PrjPcb",
        # We hard-code a ref so that this test is reproducible.
        ref="916e739f3ad9d956f4e2a293542050e1df9e6f9e",
        variant="Fitted",
    )

    assert len(components) == 945

    with open("tests/data/archimajor_components_fitted_expected.json", "r") as f:
        assert json.loads(f.read()) == components


def test_netlist_generation(request, instance):
    _setup_for_generation(
        instance,
        request.node.name,
        "https://hub.allspice.io/ProductDevelopmentFirm/ArchimajorDemo.git",
    )
    repo = instance.get_repository(
        instance.get_user().username, "-".join([test_repo, request.node.name])
    )
    netlist = generate_netlist(
        instance,
        repo,
        "Archimajor.PcbDoc",
        # We hard-code a ref so that this test is reproducible.
        ref="95719adde8107958bf40467ee092c45b6ddaba00",
    )
    assert len(netlist) == 682

    nets = list(netlist.keys())

    nets.sort()

    with open("tests/data/archimajor_netlist_expected.net", "r") as f:
        for net in nets:
            assert (net + "\n") == f.readline()
            pins_on_net = sorted(netlist[net])
            assert (" " + " ".join(pins_on_net) + "\n") == f.readline()
