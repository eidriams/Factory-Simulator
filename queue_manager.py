from collections import deque

class ProductionQueue():

    def __init__(self):

        self.queue = deque()
    
    def add_piece(self):

        self.queue.append("piece")

    def remove_piece(self):

        # If there are items in queue
        if self.queue:
            return self.queue.popleft()
        # If not
        return None
    
    def size(self):

        return len(self.queue)