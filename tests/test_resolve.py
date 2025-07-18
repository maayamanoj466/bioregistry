"""Tests for the bioregistry client."""

import unittest
from collections.abc import Iterable

import bioregistry
from bioregistry import manager
from bioregistry.resolve import get_external


class TestResolve(unittest.TestCase):
    """Tests for getting Bioregistry content."""

    def test_resolve(self):
        """Test prefixes can be resolved properly."""
        for expected, query in [
            ("ncbitaxon", "ncbitaxon"),
            ("ncbitaxon", "NCBITaxon"),
            ("ncbitaxon", "taxonomy"),
            ("scomp", "SCOMP"),
            ("sfam", "SFAM"),
            ("ec", "ec-code"),
            ("ec", "EC_CODE"),
            ("chembl.compound", "chembl.compound"),
            ("chembl.compound", "chemblcompound"),
            ("chembl", "chembl"),
        ]:
            with self.subTest(query=query):
                self.assertEqual(expected, bioregistry.normalize_prefix(query))

        with self.assertRaises(ValueError):
            bioregistry.normalize_prefix("nope", strict=True)

    def test_get(self):
        """Test getting content from the bioregistry."""
        ncbitaxon_entry = bioregistry.get_resource("ncbitaxon")
        self.assertIn("NCBI_Taxon_ID", ncbitaxon_entry.synonyms)
        self.assertIsNotNone(get_external("ncbitaxon", "miriam"))
        self.assertIsNotNone(get_external("ncbitaxon", "obofoundry"))
        self.assertIsNotNone(get_external("ncbitaxon", "ols"))
        self.assertIsNotNone(get_external("ncbitaxon", "wikidata"))

    def test_validate_true(self):
        """Test that validation returns true."""
        tests = [
            ("ec", "1"),
            ("ec", "1.1"),
            ("ec", "1.1.1"),
            ("ec", "1.1.1.1"),
            ("ec", "1.1.123.1"),
            ("ec", "1.1.1.123"),
            # Namespace in LUI: Standard rule for upper-casing
            ("chebi", "24867"),
            ("chebi", "CHEBI:1234"),
            # BANANA (explicit)
            (
                "vario",
                "0376",
            ),  # this showcases the banana problem where the namespace in LUI is weird
            ("VariO", "0376"),
            ("did", "sov:WRfXPg8dantKVubE3HX8pw"),
            ("did", "did:sov:WRfXPg8dantKVubE3HX8pw"),
            ("go.ref", "0000041"),
            ("go.ref", "GO_REF:0000041"),
            # bananas from OBO
            ("go", "0000001"),
            ("go", "GO:0000001"),
            ("go", "go:0000001"),
            # banana are strange
            ("omim.ps", "PS214100"),
            ("omim.ps", "214100"),
            ("OMIMPS", "214100"),
            ("PS", "214100"),
            ("PS", "PS214100"),
            ("agrovoc", "1234"),
            ("agrovoc", "c_1234"),
        ]
        for prefix, resource in bioregistry.read_registry().items():
            if bioregistry.is_deprecated(prefix):
                continue
            banana = bioregistry.get_banana(prefix)
            if banana is None or bioregistry.has_no_terms(prefix):
                continue
            peel = resource.get_banana_peel()
            example = bioregistry.get_example(prefix)
            with self.subTest(prefix=prefix):
                if example is None:
                    self.fail(msg=f"{prefix} has a banana {banana} but is missing an example")
                else:
                    tests.append((prefix, example))
                    tests.append((prefix, f"{banana}{peel}{example}"))
        self.assert_known_identifiers(tests)

    def assert_known_identifiers(self, examples: Iterable[tuple[str, str]]) -> None:
        """Validate the examples."""
        for prefix, identifier in examples:
            with self.subTest(prefix=prefix, identifier=identifier):
                self.assertTrue(
                    bioregistry.is_standardizable_identifier(prefix, identifier),
                    msg=f"CURIE {prefix}:{identifier} does not loosely match {bioregistry.get_pattern(prefix)}",
                )

    def test_validate_false(self):
        """Test that validation returns false."""
        for prefix, identifier in [
            ("chebi", "A1234"),
            ("chebi", "GO:A1234"),
        ]:
            with self.subTest(prefix=prefix, identifier=identifier):
                self.assertFalse(bioregistry.is_standardizable_identifier(prefix, identifier))

    def test_lui(self):
        """Test the LUI makes sense (spoilers, they don't).

        Discussion is ongoing at:

        - https://github.com/identifiers-org/identifiers-org.github.io/issues/151
        """
        for prefix in bioregistry.read_registry():
            if not bioregistry.get_namespace_in_lui(prefix):
                continue
            if bioregistry.get_banana(prefix):
                continue  # rewrite rules are applied to prefixes with bananas
            if prefix in {"ark", "obi"}:
                continue  # these patterns on identifiers.org are garb
            with self.subTest(prefix=prefix):
                re_pattern = bioregistry.get_pattern(prefix)
                miriam_prefix = bioregistry.get_identifiers_org_prefix(prefix)
                self.assertTrue(
                    re_pattern.startswith(f"^{miriam_prefix.upper()}")
                    or re_pattern.startswith(miriam_prefix.upper()),
                    msg=f"{prefix} pattern: {re_pattern}",
                )

    def test_curie_pattern(self):
        """Test CURIE pattern.

        .. seealso::

            https://github.com/biopragmatics/bioregistry/issues/245
        """
        self.assertEqual("^chebi:\\d+$", bioregistry.get_curie_pattern("chebi"))
        self.assertEqual("^CHEBI:\\d+$", bioregistry.get_curie_pattern("chebi", use_preferred=True))
        self.assertEqual(
            "^chembl\\.compound:CHEMBL\\d+$", bioregistry.get_curie_pattern("chembl.compound")
        )
        pattern = bioregistry.get_curie_pattern("panther.pthcmp")
        self.assertRegex("panther.pthcmp:P00266", pattern)
        self.assertNotRegex("pantherXpthcmp:P00266", pattern)

    def test_depends_on(self):
        """Test getting dependencies."""
        test_prefix = "foodon"
        test_target = "bfo"
        resource = bioregistry.get_resource(test_prefix)
        self.assertIsNotNone(resource)

        obofoundry = resource.get_external("obofoundry")
        self.assertIsNotNone(obofoundry)
        self.assertIn("depends_on", obofoundry)

        fobi_dependencies = manager.get_depends_on(test_prefix)
        self.assertIsNotNone(fobi_dependencies)
        self.assertIn(test_target, fobi_dependencies)

        fobi_dependencies = bioregistry.get_depends_on(test_prefix)
        self.assertIsNotNone(fobi_dependencies)
        self.assertIn(test_target, fobi_dependencies)
