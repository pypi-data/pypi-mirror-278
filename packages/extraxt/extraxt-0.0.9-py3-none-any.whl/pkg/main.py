import json

from extraxt.func.ocr import OCRService
from extraxt.func.fmt import FormatService


class Extraxt:
    def read(self, stream, type="pdf", fields=None, indent=4):
        ocr = OCRService(type=type)
        formatter = FormatService(fields=fields)

        dataframe = ocr.read(stream)
        content = dataframe.to_dict(orient="records")[0] if not dataframe.empty else {}
        data = formatter.format(content)

        output = {section.lower(): {} for section in fields.keys()}
        formatter.apply(data, output)

        return json.dumps(output, indent=indent)
