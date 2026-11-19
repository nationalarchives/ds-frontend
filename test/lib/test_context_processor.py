import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from flask import Flask

from app.lib.context_processor import icon, icon_brand, icon_brand_fw, icon_fw


class IconTestCase(unittest.TestCase):
    def setUp(self):
        root = TemporaryDirectory()
        self.addCleanup(root.cleanup)
        self.app = Flask(__name__, root_path=root.name)
        self.icons_path = Path(root.name) / "static" / "assets" / "icons"
        self.variants = (
            (icon, "solid", False),
            (icon_fw, "solid-fw", True),
            (icon_brand, "brands", False),
            (icon_brand_fw, "brands-fw", True),
        )
        for _, directory, _ in self.variants:
            path = self.icons_path / directory
            path.mkdir(parents=True)
            (path / "example.svg").write_text(
                f'<svg viewBox="0 0 24 24" data-source="{directory}">'
                '<path d="M0 0h24v24H0z"/></svg>',
                encoding="utf-8",
            )

    def test_helpers_load_matching_svg_and_add_attributes(self):
        for helper, directory, fixed_width in self.variants:
            for classes in ("", "custom-icon another-class"):
                with (
                    self.subTest(helper=helper.__name__, classes=classes),
                    self.app.app_context(),
                ):
                    svg = ElementTree.fromstring(helper("example", classes=classes))

                icon_type = "brands" if directory.startswith("brands") else "solid"
                expected_classes = ["fa", f"fa-{icon_type}", "fa-example"]
                if fixed_width:
                    expected_classes.append("fa-fw")
                expected_classes.extend(classes.split())
                self.assertCountEqual(svg.attrib["class"].split(), expected_classes)
                self.assertEqual(svg.attrib["height"], "24")
                self.assertEqual(svg.attrib["aria-hidden"], "true")
                self.assertEqual(svg.attrib["focusable"], "false")
                self.assertEqual(svg.attrib["viewBox"], "0 0 24 24")
                self.assertEqual(svg.attrib["data-source"], directory)
                self.assertEqual(svg.find("path").attrib["d"], "M0 0h24v24H0z")

    def test_icon_accepts_explicit_type_and_fixed_width(self):
        with self.app.app_context():
            svg = ElementTree.fromstring(
                icon("example", "custom-icon", type="brands", fixed_width=True)
            )

        self.assertEqual(svg.attrib["data-source"], "brands-fw")
        self.assertCountEqual(
            svg.attrib["class"].split(),
            ["fa", "fa-brands", "fa-fw", "fa-example", "custom-icon"],
        )

    def test_missing_icons_return_comment(self):
        for helper, _, _ in self.variants:
            with self.subTest(helper=helper.__name__), self.app.app_context():
                self.assertEqual(helper("missing"), "<!-- icon missing not found -->")
