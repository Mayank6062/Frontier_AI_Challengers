from ..base_exporter import BaseExporter
from ..pdf_exporter import PdfExporter
from ..docx_exporter import DocxExporter
from ..pptx_exporter import PptxExporter
from ..draw_io_exporter import DrawIoExporter
from ..yaml_exporter import YamlExporter


def test_exporters_emit_bytes_and_text() -> None:
    assert isinstance(BaseExporter().export("hello"), bytes)
    assert isinstance(PdfExporter().export("hello"), bytes)
    assert isinstance(DocxExporter().export("hello"), bytes)
    assert isinstance(PptxExporter().export("hello"), bytes)
    assert isinstance(DrawIoExporter().export("hello"), bytes)
    assert isinstance(YamlExporter().export({"topology": []}), bytes)
