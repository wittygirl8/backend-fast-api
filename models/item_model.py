from typing import List, Optional

# A simple in-memory database replacement
class ItemModel:
    def __init__(self, id: int, name: str, description: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description

# Fake in-memory database, simulating persistence
items_db: List[ItemModel] = [
    ItemModel(id=1, name="Item One", description="This is the first item."),
    ItemModel(id=2, name="Item Two", description="This is the second item."),
    ItemModel(id=3, name="Item Three", description="This is the third item."),
]

def find_item_by_id(item_id: int) -> Optional[ItemModel]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None
