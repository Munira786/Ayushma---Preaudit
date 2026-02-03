import easyocr
import pdfplumber
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, languages: list = ['en']):
        self.reader = None # Lazy load
        self.languages = languages

    def _get_reader(self):
        if self.reader is None:
            logger.info("Initializing EasyOCR...")
            self.reader = easyocr.Reader(self.languages)
        return self.reader

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """
        Extracts text from PDF or Image based on extension.
        """
        filename = filename.lower()
        
        try:
            if filename.endswith(".pdf"):
                return self._extract_from_pdf(file_bytes)
            elif filename.endswith((".jpg", ".jpeg", ".png")):
                return self._extract_from_image(file_bytes)
            elif filename.endswith(".txt"):
                return file_bytes.decode("utf-8", errors="ignore")
            else:
                logger.warning(f"Unsupported file type: {filename}")
                return ""
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            return ""

    def _extract_from_pdf(self, file_bytes: bytes) -> str:
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _extract_from_image(self, file_bytes: bytes) -> str:
        reader = self._get_reader()
        result = reader.readtext(file_bytes, detail=0)
        return " ".join(result)

ocr_engine = OCRService()
