from application import app, db, utils


if __name__ == "__main__":
	db.create_all()
	utils.add_mock_records(db)
	app.run(debug=True)
