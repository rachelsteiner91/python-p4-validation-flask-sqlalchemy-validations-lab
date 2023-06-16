from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
  ## VALIDATIONS ## 
  # 1. All authors have a name.
  # 2. No two authors have the same name. 
    @validates('name')
    def validate_name(self, key, name):
        # 1. All authors have a name.
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError('Name is required for all authors')
        # 2. No two authors have the same name.
        elif name in names:
            raise ValueError('each name within the authors is unique')
        return name

 # 3. Author phone numbers are exactly ten digits.   
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # 3. Author phone numbers are exactly ten digits so write 'if length of phone number is not equal to 10 digits'
        if len(phone_number) != 10:
            raise ValueError('Phone number must be 10 digits')
        return phone_number
        


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    
## CUSTOM VALIDATION  - 8. add a custom validator to Post model to ensure the title is sufficiently clickbait-y 
# The validator should add a validation error if the title does not contain:
# "Won't Believe" "Secret" "Top" "Guess"
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError('no clickbait found')
        return title
    
## VALIDATIONS FOR POSTS## 
## 5. Post content is at least 250 characters long.
## 6. Post summary is a maximum of 250 characters.
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if(key == 'content'):
            if len(string) <= 250:
                raise ValueError('Post content must be greater than or equal to 250 characters in length')
        if(key == 'summary'):
            if len(string) >= 250:
                raise ValueError('Post summary must be less than or equal to 250 characters in length')
        return string
    
# 7. Post category is either Fiction or Non-Fiction.
    @validates('category')
    def validate_category(self, key, category):
        # if category is not equal to Fiction or Non-Fiction, raise error
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('category must be Fiction or Non-Fiction')
        return category

