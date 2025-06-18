

class PagedResponse[T]:
    def __init__(self, data: list[T], page: int, page_size: int, total: int):
        self.data = data
        self.page = page
        self.page_size = page_size
        self.total = total

    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

# Example Usage
paged_response = PagedResponse[str](data=["item1", "item2"], page=1, page_size=2, total=5)
print(f"Page {paged_response.page} of {paged_response.total_pages()}")
print("Data:", paged_response.data)
