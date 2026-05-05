from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cemetery.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    name = request.args.get('name', '')

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT 
            record_id,
            full_name,
            birth_date,
            death_date,
            section,
            plot_number,
            veteran_status,
            headstone_condition,
            notes
        FROM graves
        WHERE full_name LIKE ?
        ORDER BY full_name
    """, (f'%{name}%',)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

@app.route('/geojson')
def geojson():
    name = request.args.get('name', '')

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT 
            record_id,
            full_name,
            birth_date,
            death_date,
            section,
            plot_number,
            latitude,
            longitude,
            veteran_status,
            headstone_condition,
            notes
        FROM graves
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
        AND full_name LIKE ?
        ORDER BY full_name
    """, (f'%{name}%',)).fetchall()
    conn.close()

    features = []

    for row in rows:
        features.append({
            "type": "Feature",
            "properties": {
                "record_id": row["record_id"],
                "full_name": row["full_name"],
                "birth_date": row["birth_date"],
                "death_date": row["death_date"],
                "section": row["section"],
                "plot_number": row["plot_number"],
                "veteran_status": row["veteran_status"],
                "headstone_condition": row["headstone_condition"],
                "notes": row["notes"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    row["longitude"],
                    row["latitude"]
                ]
            }
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })

if __name__ == '__main__':
    app.run(debug=True)