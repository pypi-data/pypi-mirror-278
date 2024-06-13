"""
Utility routes to run full text search on Kitsu data.
"""

from flask import Blueprint
from StudioPulse.app.utils.api import configure_api_from_blueprint

from StudioPulse.app.blueprints.search.resources import SearchResource

routes = [("/data/search", SearchResource)]

blueprint = Blueprint("search", "search")
api = configure_api_from_blueprint(blueprint, routes)
