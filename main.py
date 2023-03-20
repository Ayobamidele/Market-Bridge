from supply_bridge import app, db

from supply_bridge.models import *

@app.shell_context_processor
def make_shell_context():
    return {x[0]:x[1] for x in db.metadata.tables.items()}

if __name__ == "__main__":
    app.run(debug=True)
