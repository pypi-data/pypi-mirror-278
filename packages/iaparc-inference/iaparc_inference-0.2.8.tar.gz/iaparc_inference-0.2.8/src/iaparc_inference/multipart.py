"""
IA Parc Inference service
Support for multipart data
"""
from io import BytesIO
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import BaseTarget, ValueTarget, FileTarget, NullTarget


class BinaryTarget(BaseTarget):
    """BinaryTarget writes (streams) the input to an io.BytesIO handler."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fd = None

    def on_start(self):
        self._fd = BytesIO()

    def on_data_received(self, chunk: bytes):
        if self._fd:
            self._fd.write(chunk)

    def on_finish(self):
        if self._fd:
            self._fd.seek(0)
    
    @property
    def file(self):
        return self._fd