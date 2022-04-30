from server import app, db
from server.models import *
from datetime import datetime, date
import random

@app.route('/create')
def create_route():
    Bin.query.delete()
    BinData.query.delete()
    Distances.query.delete()
    db.session.commit()

    numBins = 30
    for i in range(1, numBins):
        db.session.add(Bin(**{"id": i, "location": f"location #{i}", "fill_rate": random.randint(10, 100)}))

    for i in range(1, numBins):
        db.session.add(BinData(
            **{
                "bin_id": i,
                "date_time": datetime.now(),
                "distance": random.randint(5, 40),
                "temperature": random.randint(25, 40),
                "humidity": random.randint(50, 100)
            }
        ))

    for i in range(1, numBins):
        for j in range(1, numBins):
            if i != j:
                db.session.add(Distances(
                    **{
                        "bin_one": i,
                        "bin_two": j,
                        "distance": random.randint(100, 500)
                    }
                ))

    db.session.commit()
    return """
    <nav>
        <a href="/">home</a><br/>
        <a href="/create">create new dataset</a><br/>
        <a href="/make-route">see optimal route</a><br/>
        <a href="/view-db">view db</a><br/>
    </nav>
    """