from flask import Blueprint, jsonify
from scraper.database import get_posts

api=Blueprint("api",__name__)

@api.route("/api/posts",methods=["GET"])
def posts():
    posts = get_posts()
    return jsonify(posts)
