import os
import subprocess

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def process(self,output_dir):
        # Example: pretend to process the PDF and output some files
        try:
            subprocess.run(['marker_single', self.pdf_path, output_dir], check=True)
            print(f"Processed {self.pdf_path} and created files in {output_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error running marker_single: {e}")
            return
        
      
    
      

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <pdf_file> <output_dir>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_dir = sys.argv[2]
    processor = PDFProcessor(pdf_file)
    processor.process(output_dir)

if __name__ == "__main__":
    main()
