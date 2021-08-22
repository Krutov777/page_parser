import os


class ContentStorage:
    """storage class"""
    def __init__(self, content_for_save, path):
        self.content_for_save = content_for_save
        self.path = path
    
    def save(self):
        """Save content to file."""
        mode = 'w' if isinstance(self.content_for_save, str) else 'wb'
        with open(self.path, mode) as file_descriptor:
            file_descriptor.write(self.content_for_save)
    
    def create_dir(self):
        """Create dir if dit is not exists."""
        if not os.path.exists(self.path):
            os.mkdir(self.path)
