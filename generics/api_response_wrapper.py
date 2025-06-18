class ApiResponse[T,U]:
    def __init__(self,data:T,status:U):
        self.data = data
        self.status = status


    def get_data(self) -> T:
        return self.data
    
    def get_status(self) -> U:
        return self.status
    

response = ApiResponse[str,int]("Success", 200)

print(response.get_data())
print(response.get_status())