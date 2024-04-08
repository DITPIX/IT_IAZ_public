from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
db = SQLAlchemy(app)

class AnalyticalReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(255), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    report_description = db.Column(db.Text)
    author = db.Column(db.String(100))
    recommendation = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'report_name': self.report_name,
            'report_date': str(self.report_date),
            'report_description': self.report_description,
            'author': self.author,
            'recommendation': self.recommendation
        }

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = AnalyticalReport.query.all()
    return jsonify([report.to_dict() for report in reports]), 200

@app.route('/reports/<int:id>', methods=['GET'])
def get_report(id):
    report = AnalyticalReport.query.get(id)
    if report:
        return jsonify(report.to_dict()), 200
    else:
        return jsonify({'error': 'Report not found'}), 404

@app.route('/reports', methods=['POST'])
def create_report():
    data = request.json
    try:
        report = AnalyticalReport(
            report_name=data['report_name'],
            report_date=data['report_date'],
            report_description=data['report_description'],
            author=data['author'],
            recommendation=data['recommendation']
        )
        db.session.add(report)
        db.session.commit()
        return jsonify(report.to_dict()), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Duplicate report name'}), 400

@app.route('/reports/<int:id>', methods=['PUT'])
def update_report(id):
    report = AnalyticalReport.query.get(id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    data = request.json
    try:
        report.report_name = data['report_name']
        report.report_date = data['report_date']
        report.report_description = data['report_description']
        report.author = data['author']
        report.recommendation = data['recommendation']
        db.session.commit()
        return jsonify(report.to_dict()), 200
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400

@app.route('/reports/<int:id>', methods=['DELETE'])
def delete_report(id):
    report = AnalyticalReport.query.get(id)
    if report:
        db.session.delete(report)
        db.session.commit()
        return jsonify({'message': 'Report deleted successfully'}), 200
    else:
        return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
