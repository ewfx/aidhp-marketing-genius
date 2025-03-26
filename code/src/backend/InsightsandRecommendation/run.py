import os
from app.init import create_app
port = int(os.environ.get('PORT', 8080))
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
