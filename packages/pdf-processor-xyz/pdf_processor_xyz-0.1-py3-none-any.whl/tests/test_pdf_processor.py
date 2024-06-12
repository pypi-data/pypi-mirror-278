import unittest
from my_pdf_package.pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def test_process(self):
        processor = PDFProcessor("dummy.pdf")
        output_files = processor.process()
        self.assertEqual(len(output_files), 2)

if __name__ == '__main__':
    unittest.main()
