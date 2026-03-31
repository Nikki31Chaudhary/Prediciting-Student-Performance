from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, default_limits=["300 per day", "60 per hour"])
cors = CORS()