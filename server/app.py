import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Import our database and models
from models import db, User, Task

app = Flask(__name__)

# Basic Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here' # In a real app, use an env variable

# Initialize Extensions
migrate = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

# --- AUTH ROUTES ---

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=data.get('username')).first()
        if user_exists:
            return {"error": "User already exists"}, 422
            
        try:
            new_user = User(username=data.get('username'))
            # This triggers the password_hash setter in models.py
            new_user.password_hash = data.get('password')
            
            db.session.add(new_user)
            db.session.commit()
            
            # Create token so they are logged in immediately
            token = create_access_token(identity=new_user.id)
            return {"user": new_user.to_dict(), "token": token}, 201
            
        except Exception as e:
            return {"error": str(e)}, 422

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.authenticate(data.get('password')):
            token = create_access_token(identity=user.id)
            return {"user": user.to_dict(), "token": token}, 200
        
        return {"error": "Invalid username or password"}, 401

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        # This gets the user ID from the JWT token sent in the header
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if user:
            return user.to_dict(), 200
        return {"error": "Not authorized"}, 401

# --- TASK RESOURCES ---

class TaskList(Resource):
    @jwt_required()
    def get(self):
        # Get current user
        user_id = get_jwt_identity()
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Query only the tasks belonging to this user
        tasks_query = Task.query.filter_by(user_id=user_id)
        
        # Apply pagination
        paginated_tasks = tasks_query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "tasks": [t.to_dict() for t in paginated_tasks.items],
            "total": paginated_tasks.total,
            "pages": paginated_tasks.pages,
            "current_page": paginated_tasks.page
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        try:
            new_task = Task(
                title=data.get('title'),
                description=data.get('description'),
                importance=data.get('importance'),
                category=data.get('category'),
                user_id=user_id 
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

class TaskByID(Resource):
    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()
        # Ensure task exists AND belongs to the user
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        
        if not task:
            return {"error": "Task not found or unauthorized"}, 404

        data = request.get_json()
        for attr in data:
            setattr(task, attr, data[attr])
        
        db.session.commit()
        return task.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        
        if not task:
            return {"error": "Task not found or unauthorized"}, 404

        db.session.delete(task)
        db.session.commit()
        return {}, 204

# Register Resources
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/me')
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskByID, '/tasks/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)