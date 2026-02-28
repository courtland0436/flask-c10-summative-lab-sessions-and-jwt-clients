from app import app
from models import db, User, Task
from faker import Faker
import random

fake = Faker()

def seed_database():
    with app.app_context():
        print("Deleting existing data...")
        Task.query.delete()
        User.query.delete()

        print("Creating users...")
        users = []
        # Create a specific test user we can use to log in
        test_user = User(username="developer")
        test_user.password_hash = "password123"
        users.append(test_user)

        # Create 4 more random users
        for _ in range(4):
            user = User(username=fake.user_name())
            user.password_hash = "password"
            users.append(user)
        
        db.session.add_all(users)
        db.session.commit()

        print("Creating tasks...")
        tasks = []
        categories = ["Work", "Personal", "Urgent", "School"]
        
        for user in users:
            # Give each user 3-5 random tasks
            for _ in range(random.randint(3, 5)):
                task = Task(
                    title=fake.catch_phrase(),
                    description=fake.sentence(),
                    importance=random.randint(1, 5),
                    category=random.choice(categories),
                    user=user
                )
                tasks.append(task)
        
        db.session.add_all(tasks)
        db.session.commit()

        print("Seeding complete!")

if __name__ == '__main__':
    seed_database()