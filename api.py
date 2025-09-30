"""
A simple Flask API to expose the aggregated business‑intelligence data.

Endpoints:
  - `/providers`          : Return a list of providers with summary metrics.
  - `/providers/<name>`   : Return summary data for a specific provider.

The API reads from a SQLite database (`healthcare_bi.db`) created by `analysis.py`.
"""

from flask import Flask, jsonify, abort
import sqlite3

DB_PATH = 'healthcare_bi.db'

app = Flask(__name__)


def query_db(query, args=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results


@app.route('/providers', methods=['GET'])
def get_providers():
    data = query_db('SELECT * FROM provider_summary')
    return jsonify(data)


@app.route('/providers/<provider_name>', methods=['GET'])
def get_provider(provider_name):
    data = query_db('SELECT * FROM provider_summary WHERE referral_provider = ?', (provider_name,))
    if not data:
        abort(404, description='Provider not found')
    return jsonify(data[0])


if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)