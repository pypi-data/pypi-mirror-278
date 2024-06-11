from typing import Any, Mapping

import send_s3.actions.log as log
import send_s3.actions.init as init
import send_s3.actions.upload as upload


ACTIONS: Mapping[str, Any] = {
    'log': log,
    'upload': upload,
    'init': init,
}

__all__ = ['ACTIONS']
