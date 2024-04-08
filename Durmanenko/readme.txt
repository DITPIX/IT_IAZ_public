project 1
Ось невеликий приклад коду для створення таблиці в базі даних PostgreSQL за допомогою мови SQL. В цьому прикладі ми створюємо таблицю для зберігання даних про аналітичні звіти у сфері оборони:

```sql
CREATE TABLE analytical_reports (
    id SERIAL PRIMARY KEY,
    report_name VARCHAR(255) NOT NULL,
    report_date DATE NOT NULL,
    report_description TEXT,
    author VARCHAR(100),
    recommendation TEXT,
    CONSTRAINT unique_report_name UNIQUE (report_name)
);
```

Опис полів у таблиці:

- `id`: унікальний ідентифікатор аналітичного звіту (автоматично збільшується для кожного нового запису).
- `report_name`: назва аналітичного звіту (обов'язкове поле, обмежене до 255 символів).
- `report_date`: дата аналітичного звіту (обов'язкове поле).
- `report_description`: опис аналітичного звіту (текстове поле, може містити довільну кількість символів).
- `author`: автор аналітичного звіту (текстове поле, обмежене до 100 символів).
- `recommendation`: рекомендації, що містяться в аналітичному звіті (текстове поле, може містити довільну кількість символів).

Таким чином, цей код дозволяє створити таблицю `analytical_reports` для зберігання аналітичних звітів у сфері оборони з обраною структурою. Не забудьте налаштувати вашу базу даних PostgreSQL та забезпечити її взаємодію з вашим додатком, написаним на Python з використанням Django або Flask.

Звичайно, ви можете використати один SQL-запит для вставки 20 рядків в таблицю `analytical_reports`. Ось приклад SQL-запиту, який вставляє 20 варіантів значень за один раз:

```sql
INSERT INTO analytical_reports (report_name, report_date, report_description, author, recommendation) VALUES
('Report 1', '2023-01-15', 'Description 1', 'Author 1', 'Recommendation 1'),
('Report 2', '2023-02-20', 'Description 2', 'Author 2', 'Recommendation 2'),
('Report 3', '2023-03-25', 'Description 3', 'Author 3', 'Recommendation 3'),
('Report 4', '2023-04-30', 'Description 4', 'Author 4', 'Recommendation 4'),
('Report 5', '2023-05-05', 'Description 5', 'Author 5', 'Recommendation 5'),
('Report 6', '2023-06-10', 'Description 6', 'Author 6', 'Recommendation 6'),
('Report 7', '2023-07-15', 'Description 7', 'Author 7', 'Recommendation 7'),
('Report 8', '2023-08-20', 'Description 8', 'Author 8', 'Recommendation 8'),
('Report 9', '2023-09-25', 'Description 9', 'Author 9', 'Recommendation 9'),
('Report 10', '2023-10-30', 'Description 10', 'Author 10', 'Recommendation 10'),
('Report 11', '2023-11-05', 'Description 11', 'Author 11', 'Recommendation 11'),
('Report 12', '2023-12-10', 'Description 12', 'Author 12', 'Recommendation 12'),
('Report 13', '2023-01-15', 'Description 13', 'Author 13', 'Recommendation 13'),
('Report 14', '2023-02-20', 'Description 14', 'Author 14', 'Recommendation 14'),
('Report 15', '2023-03-25', 'Description 15', 'Author 15', 'Recommendation 15'),
('Report 16', '2023-04-30', 'Description 16', 'Author 16', 'Recommendation 16'),
('Report 17', '2023-05-05', 'Description 17', 'Author 17', 'Recommendation 17'),
('Report 18', '2023-06-10', 'Description 18', 'Author 18', 'Recommendation 18'),
('Report 19', '2023-07-15', 'Description 19', 'Author 19', 'Recommendation 19'),
('Report 20', '2023-08-20', 'Description 20', 'Author 20', 'Recommendation 20');
```

Цей запит вставляє 20 рядків одночасно в таблицю `analytical_reports`. Вам потрібно буде замінити значення `report_name`, `report_date`, `report_description`, `author` та `recommendation` на ваші власні дані.


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
