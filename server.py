from waitress import serve
import app
from settings import FLASK_PORT

serve(app.app, host='0.0.0.0', port=FLASK_PORT)
