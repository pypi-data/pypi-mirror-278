import uuid

from JaysAppManager.functions.cryptography import get_key



class RunManager:
    def __init__(self):
        self._run_id = None

    def set_run_id(self):
        get_key()
        self._run_id = str(uuid.uuid4())  # Generate a unique run ID

    def get_run_id(self):
        return self._run_id
    

