from src.backend.output_generation.export.base_exporter import BaseExporter
from src.backend.output_generation.export.pdf_exporter import PdfExporter
from src.backend.output_generation.export.docx_exporter import DocxExporter
from src.backend.output_generation.export.pptx_exporter import PptxExporter
from src.backend.output_generation.export.draw_io_exporter import DrawIoExporter
from src.backend.output_generation.export.yaml_exporter import YamlExporter


def test_exporters_emit_bytes_and_text() -> None:
    assert isinstance(BaseExporter().export("hello"), bytes)
    assert isinstance(PdfExporter().export("hello"), bytes)
    assert isinstance(DocxExporter().export("hello"), bytes)
    assert isinstance(PptxExporter().export("hello"), bytes)
    assert isinstance(DrawIoExporter().export("hello"), bytes)
    assert isinstance(YamlExporter().export({"topology": []}), str)
