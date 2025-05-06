from flask_restful import Resource, reqparse, fields, marshal_with, abort
from werkzeug.utils import secure_filename
import werkzeug
import os
import django
from datetime import datetime
import sys
# import threading

# Setup Django environment
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quillwave.settings')
django.setup()

# db_lock = threading.Lock()

from posts.models import Post
from django.contrib.auth.models import User

# Serialization fields
post_fields = {
    'id': fields.Integer,
    'author_id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'image': fields.String,
    'is_draft': fields.Boolean,
    'created_at': fields.String,
}

# Request parsers


post_parser = reqparse.RequestParser()
post_parser.add_argument('title',    required=True, help="Title cannot be blank.", location='form')
post_parser.add_argument('body',     required=True, help="Body cannot be blank.",  location='form')
post_parser.add_argument('is_draft', type=bool,                                     location='form')
post_parser.add_argument('author_id',type=int,   required=True, help="Author ID required.", location='form')
post_parser.add_argument('image',    type=werkzeug.datastructures.FileStorage,     location='files')

class PostListAPI(Resource):
    @marshal_with(post_fields)
    def get(self):
        return Post.objects.filter(is_draft=False).order_by('-created_at')

    @marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        user = User.objects.get(pk=args['author_id'])

        # Forcefully convert string to boolean
        is_draft_raw = args.get('is_draft')
        is_draft = str(is_draft_raw).lower() in ['true', '1', 'yes']

        post = Post(
            author=user,
            title=args['title'],
            body=args['body'],
            is_draft=is_draft
        )

        if args.get('image'):
            filename = secure_filename(args['image'].filename)
            filepath = os.path.join(project_path, 'media', 'post_images', filename)
            args['image'].save(filepath)
            post.image = 'post_images/' + filename
        # with db_lock:
        post.save()
        return post, 201

class PostAPI(Resource):
    @marshal_with(post_fields)
    def get(self, post_id):
        post = Post.objects.filter(pk=post_id).first() or abort(404, message="Post not found")
        return post

    @marshal_with(post_fields)
    def put(self, post_id):
        post = Post.objects.filter(pk=post_id).first() or abort(404)
        args = post_parser.parse_args()
        post.title = args['title']
        post.body = args['body']
        post.is_draft = args.get('is_draft', post.is_draft)
        if args.get('image'):
            filename = secure_filename(args['image'].filename)
            filepath = os.path.join(project_path, 'media', 'post_images', filename)
            args['image'].save(filepath)
            post.image = 'post_images/' + filename
        # with db_lock:
        post.save()
        return post

    def delete(self, post_id):
        post = Post.objects.filter(pk=post_id).first() or abort(404)
        # with db_lock:
        post.delete()
        return {'message': 'Deleted'}, 204
    
    
    
