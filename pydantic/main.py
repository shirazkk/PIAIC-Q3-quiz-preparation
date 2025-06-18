"""

1. Basic Model
Create a simple Pydantic model User with the fields name (string) and age (integer).

The age should be an integer that represents the user's age.

"""

from pydantic import BaseModel, Field,  validator, ValidationError
from pydantic_settings import BaseSettings

# class User(BaseModel):
#     name:str
#     age:int

# user = User(name="jack",age=12)
# print(user.name)
# print(user.age)


"""

2. Field Validation
Create a Pydantic model Product with the following fields:

name (string)

price (float)

quantity (integer)

Add validation to ensure:

The price is greater than 0.

The quantity is at least 1.

"""

# class Product(BaseModel):
#     name:str
#     price: float = Field(...,gt=0)
#     quantity: int= Field(max=1)


# product = Product(name="iphone-12",price=2,quantity=12)
# print(product)


"""

3. Nested Models
Create two models:

Address with the fields street (string), city (string), and zip_code (string).

UserProfile with the fields user_name (string) and address (a nested Address model).

Create an instance of UserProfile with a nested Address.

"""

# class Address(BaseModel):
#     street:str
#     city:str
#     zip_code:str

# class UserProfile(BaseModel):
#     user_name:str
#     address: Address

# address1 = Address(street="a-11",city="karachi",zip_code="2s44")
# profile1 = UserProfile(user_name="jack",address=address1)

# print(profile1)


"""

4. JSON Serialization
Create a Pydantic model Car with fields:

make (string)

model (string)

year (integer)

Serialize the Car model to JSON using .json() and then parse it back using .parse_raw().

"""

# class Car(BaseModel):
#     make:str
#     model:str
#     year:int

# car = Car(make="Toyota",model="g-wagon",year=2026)

# print(car.json())

# print(Car.parse_raw(car.json()))


"""

5. Settings Management
Create a Settings model that has the following fields:

app_name (string)

debug_mode (boolean)

database_url (string)

Use environment variables for app_name and database_url. Set default values for other fields

"""

# class Settings(BaseSettings):
#     app_name:str 
#     debug_mode:bool = False
#     database_url:str

#     class Config:
#         env_file = ".env"


# settings = Settings()

# print(f"App Name: {settings.app_name}")
# print(f"Debug Mode: {settings.debug_mode}")
# print(f"Database URL: {settings.database_url}")



"""

6. Real-World Example
Create a BlogPost model with the following fields:

title (string)

content (string)

author (string)

Ensure that:

content has a minimum length of 50 characters.

title must start with the word "Blog:".

"""

# class BlogPost(BaseModel):
#     tittle:str 
#     content:str = Field(...,min_length=50)
#     author:str


#     @validator("tittle")
#     def validate_tittle(cls,v):
#         if not v.startswith("Blog"):
#             raise ValueError("title must start with the word 'Blog' ")
#         return v
# try:
#     blog = BlogPost(tittle="Blog car",content="hjdaskjdjkadjksajdsajkbdkjabskjdbsakjbdkjsabdkjbsakjdbjsakbdkjsabkjdbsakjbdkjsabkjdbsakjdbkjsabdkjs",author="jack")
#     print(blog)
# except ValidationError as ve:
#     print(f"Error: {ve}")