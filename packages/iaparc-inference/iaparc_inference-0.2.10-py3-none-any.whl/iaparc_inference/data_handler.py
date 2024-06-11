"""
IA Parc Inference data handler
"""
import os
import io
import logging
import logging.config
from tkinter import E
#from PIL import Image
from PIL.Image import Image
from io import BytesIO
#from typing import Any

Error = ValueError | None

LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=LEVEL,
    force=True,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("Inference")
LOGGER.propagate = True


class DataHandler():
    """
    Data Handler
    This a read-only class that handles the data
    """

    def __init__(self, data: bytes, content_type: str, parameters: dict, conf: dict, uid: str, source: str, is_input: bool = True):
        """
        Constructor
        Arguments:
        
        """
        self._raw = data
        self._content_type = content_type
        self._conf = conf
        self._name = conf["name"]
        self._parameters = parameters
        self._uid = uid
        self._source = source
        self._items = {}       
        ## Init to None data kinds
        self._file: BytesIO | None = None
        self._text: str | None = None
        self._image: Image | None = None
        # self._audio  | None= None
        # self._video | None= None
        self._json: dict | None = None
        #self._table = None
        self._is_multi = self._conf["type"] == "multimodal"
        self.error: Error = None
        self.init_items()
    
    def init_items(self):
        self.items
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def items(self) -> dict:
        if self._is_multi:
            if not self._items:
                self._items, self.error = _read_multi_part(self._raw, self._conf["items"], self._content_type)
            return self._items
        else:
            if not self._items:
                match self._conf["type"]:
                    case "file":
                        self._items[self.name] = self.file
                    case "text":
                        self._items[self.name] = self.text
                    case "image":
                        self._items[self.name] = self.image
                    case "json":
                        self._items[self.name] = self.json
                    case _:
                        self._items[self.name] = self._raw
                self._items[self.name] = self
            return self._items
    
    @property
    def raw_data(self) -> bytes:
        return self._raw
    @property
    def parameters(self) -> dict:
        return self._parameters
    
    @property
    def file(self) -> BytesIO | None:
        if self._is_multi or self._conf["type"] not in ["file", "image", "binary", "audio", "video"]:
            return None
        if not self._file:
            self._file, self.error = _read_file(self._raw)
        return self._file
        
    @property
    def text(self) -> str | None:
        if self._is_multi or self._conf["type"] != "text":
            return None
        if not self._text:
            self._text, self.error = _read_text(self._raw)
        return self._text
    
    @property
    def image(self) -> Image | None:
        if self._is_multi or self._conf["type"] != "image":
            return None
        if not self._image:
            self._image, self.error = _read_image(self._raw)
        return self._image
    
    @property
    def json(self) -> dict | None:
        if self._is_multi or self._conf["type"] != "json":
            return None
        if not self._json:
            self._json, self.error = _read_json(self._raw)
        return self._json



## Data readers

def _read_file(data: bytes) -> tuple[BytesIO, Error]:
    """
    Read file
    Arguments:
    data: bytes
    """
    if not data:
        return BytesIO(), ValueError("No data to read")
    if not isinstance(data, bytes):
        return BytesIO(), ValueError("Data is not bytes")
    try:
        file = io.BytesIO(data)
    except Exception as e:
        return BytesIO(), ValueError(f"Error reading file: {e}")
    return file, None

def _read_image(data: bytes) -> tuple[Image|None, Error]:
    """
    Read image
    Arguments:
    data: bytes
    """
    if not data:
        return None, ValueError("No data to read")
    if not isinstance(data, bytes):
        return None, ValueError("Data is not bytes")
    try:
        from PIL import Image
        image = Image.open(io.BytesIO(data))
    except Exception as e:
        return None, ValueError(f"Error reading image: {e}")    
    return image, None

def _read_text(data: bytes) -> tuple[str, Error]:
    """
    Read text
    Arguments:
    data: bytes
    """
    if not data:
        return "", ValueError("No data to read")
    if not isinstance(data, bytes):
        return "", ValueError("Data is not bytes")
    try:
        text = data.decode("utf-8")
    except Exception as e:
        return "", ValueError(f"Error reading text: {e}")
    return text, None

def _read_json(data: bytes) -> tuple[dict, Error]:
    """
    Read json
    Arguments:
    data: bytes
    """
    if not data:
        return {}, ValueError("No data to read")
    if not isinstance(data, bytes):
        return {}, ValueError("Data is not bytes")
    try:
        import json
        json_data = json.loads(data)
    except Exception as e:
        return {}, ValueError(f"Error reading json: {e}")
    return json_data, None
    
def _read_multi_part(data: bytes, items: list, content_type: str) -> tuple[dict, Error]:
    """
    Read multi-part data
    Arguments:
    data: bytes
    """
    if not data:
        return {}, ValueError("No data to read")
    if not isinstance(data, bytes):
        return {}, ValueError("Data is not bytes")
    if not items:
        return {}, ValueError("No items to read")
    try:        
        from streaming_form_data import StreamingFormDataParser
        from streaming_form_data.targets import BaseTarget

        class BytesTarget(BaseTarget):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._data = None
                
            def on_data_received(self, data: bytes):
                self.data = data

        results = {}
        if "boundary" not in content_type:
            boundary = _get_boundary(data)
            if boundary:
                content_type += f'; boundary={boundary}'
        
        headers = {'Content-Type': content_type}
        #headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}
        parser = StreamingFormDataParser(headers=headers)
        for item in items:
            results[item["name"]] = BytesTarget()                
            parser.register(item["name"], results[item["name"]])

        parser.data_received(data)
        
        for item in items:
            results[item["name"]] = DataHandler(results[item["name"]].data, content_type, {}, item, "", "", True)
            if results[item["name"]].error:
                return {}, results[item["name"]].error
    except Exception as e:
        return {}, ValueError(f"Error reading multi-part data: {e}")
    return results, None

def _read_audio(data: bytes):
    """
    Read audio
    Arguments:
    data: bytes
    """
    pass


def _get_boundary(data: bytes) -> str | None:
    """
    Get boundary
    Arguments:
    data: bytes
    """
    splitted = data.split(b"\r\n")
    if len(splitted) < 2:
        return None
    boundary = splitted[0]
    if len(boundary) < 2:
        return None
    return boundary[2:].decode("utf-8")