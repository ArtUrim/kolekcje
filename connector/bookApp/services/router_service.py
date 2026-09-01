import os
import uuid


class RouterService:
    def __init__(self, shared_dir):
        self.shared_dir = shared_dir

    def create_restart_trigger(self):
        os.makedirs(self.shared_dir, exist_ok=True)
        trigger_filename = f"task_{uuid.uuid4().hex}.trigger"
        trigger_filepath = os.path.join(self.shared_dir, trigger_filename)
        with open(trigger_filepath, 'w') as f:
            f.write("run")
        return trigger_filename
