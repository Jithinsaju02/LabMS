@app.route('/bookequipment')
# @login_required
# def bookequipment():
#     if request.method == 'POST':
#         equipmentname = request.form['ename']
#         username = request.form['username']
#         lab = request.form['lab']
#         date = request.form['date']
#         from_time = request.form['from_time']
#         to_time = request.form['to_time']
#         labs = Labs.query.filter_by(username=username).first()
#         conflicting_booking = Labs.query.filter_by(labname=lab, date=date).filter(
#             (Labs.from_time <= from_time) & (Labs.to_time > from_time) |
#             (Labs.from_time < to_time) & (Labs.to_time >= to_time) |
#             (Labs.from_time >= from_time) & (Labs.to_time <= to_time)
#         ).first()
#         if conflicting_booking:
#             flash("Lab is already booked for the given time slot")
#             return redirect(url_for('booklab'))
#         new_user = Users(username=username, lab=lab, date=date, from_time=from_time,  to_time= to_time)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("User created successfully")
#         return redirect(url_for('login'))
#     return render_template('book_equipment.html')