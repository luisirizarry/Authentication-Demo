from app import db
from models import User, Feedback

# Create all tables
db.drop_all()
db.create_all()

# Sample users
user1 = User.register(
    username="john_doe",
    pwd="password123",
    email="john@example.com",
    first_name="John",
    last_name="Doe"
)

user2 = User.register(
    username="jane_smith",
    pwd="securepwd",
    email="jane@example.com",
    first_name="Jane",
    last_name="Smith"
)

user3 = User.register(
    username="mark_watson",
    pwd="mypassword",
    email="mark@example.com",
    first_name="Mark",
    last_name="Watson"
)

# Add users to the session
db.session.add_all([user1, user2, user3])
db.session.commit()

# Sample feedback
feedback1 = Feedback(
    title="Great service",
    content="I had a great experience using this product!",
    username=user1.username
)

feedback2 = Feedback(
    title="Feedback Title",
    content="Here's some detailed feedback.",
    username=user2.username
)

feedback3 = Feedback(
    title="Suggestion",
    content="It would be nice if the product had more features.",
    username=user3.username
)

# Add feedback to the session
db.session.add_all([feedback1, feedback2, feedback3])
db.session.commit()
