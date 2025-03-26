import os
import csv
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.room import Room
from app.models.reservation import Reservation
from app.forms.room_forms import RoomForm

# Configuration for file uploads
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

admin = Blueprint('admin', __name__)

# Admin middleware to check if user is admin
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Vous n\'avez pas les autorisations nécessaires pour accéder à cette page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/admin')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get pending reservations
    pending_reservations = Reservation.query.filter_by(status='en attente').order_by(Reservation.created_at.desc()).all()
    # Get all rooms
    rooms = Room.query.all()

    return render_template(
        'admin/dashboard.html',
        title='Tableau de bord administrateur',
        pending_reservations=pending_reservations,
        rooms=rooms
    )

@admin.route('/admin/rooms/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_room():
    """Add a new room"""
    form = RoomForm()

    if form.validate_on_submit():
        room = Room(
            name=form.name.data,
            capacity=form.capacity.data,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(room)
        db.session.commit()
        flash('La salle a été ajoutée avec succès !', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_room.html', title='Ajouter salle', form=form)


@admin.route('/admin/rooms/add-many', methods=['GET', 'POST'])
@login_required
@admin_required
def add_rooms_from_csv():
    """Add many rooms from a csv file"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'csv_file' not in request.files:
            flash('Aucun fichier trouvé.', 'danger')
            return redirect(request.url)

        csv_file = request.files['csv_file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if csv_file.filename == '':
            flash('Aucun fichier sélectionné.', 'danger')
            return redirect(request.url)

        if csv_file and allowed_file(csv_file.filename):
            filename = secure_filename(csv_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            csv_file.save(filepath)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rooms_added = 0

                    for row in reader:
                        # Check if all required fields are present
                        if all(key in row for key in ['name', 'capacity', 'location']):
                            try:
                                # Convert capacity to integer
                                capacity = int(row['capacity'])

                                # Create room object
                                room = Room(
                                    name=row['name'],
                                    capacity=capacity,
                                    location=row['location'],
                                    description=row.get('description', '')  # Description is optional
                                )
                                db.session.add(room)
                                rooms_added += 1
                            except ValueError:
                                # If capacity is not a valid integer
                                flash(f"Erreur: La capacité '{row.get('capacity')}' pour la salle '{row.get('name')}' n'est pas un nombre valide.", 'danger')
                        else:
                            # If required fields are missing
                            missing = [field for field in ['name', 'capacity', 'location'] if field not in row]
                            flash(f"Erreur: Champs manquants {', '.join(missing)} dans une ligne du CSV.", 'danger')

                    if rooms_added > 0:
                        db.session.commit()
                        flash(f'{rooms_added} salles ont été ajoutées avec succès !', 'success')
                    else:
                        flash('Aucune salle n\'a été ajoutée. Vérifiez le format du fichier CSV.', 'warning')
            except Exception as e:
                db.session.rollback()
                flash(f'Erreur lors de l\'importation: {str(e)}', 'danger')

            # Clean up the uploaded file
            try:
                os.remove(filepath)
            except:
                pass

            return redirect(url_for('admin.dashboard'))
        else:
            flash('Type de fichier non autorisé. Veuillez utiliser un fichier CSV.', 'danger')

    return render_template('admin/add_rooms_from_csv.html', title='Ajouter des salles à partir d\'un fichier CSV')


@admin.route('/admin/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(room_id):
    """Edit a room"""
    room = Room.query.get_or_404(room_id)
    form = RoomForm()

    if form.validate_on_submit():
        room.name = form.name.data
        room.capacity = form.capacity.data
        room.location = form.location.data
        room.description = form.description.data
        db.session.commit()
        flash('La salle a été mise à jour avec succès !', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.name.data = room.name
        form.capacity.data = room.capacity
        form.location.data = room.location
        form.description.data = room.description

    return render_template('admin/edit_room.html', title='Modifier salle', form=form, room=room)

@admin.route('/admin/rooms/<int:room_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_room(room_id):
    """Delete a room"""
    room = Room.query.get_or_404(room_id)

    # Check if room has any reservations
    if room.reservations:
        flash('Impossible de supprimer une salle avec des réservations existantes.', 'danger')
        return redirect(url_for('admin.dashboard'))

    db.session.delete(room)
    db.session.commit()
    flash('La salle a été supprimée avec succès !', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/reservations')
@login_required
@admin_required
def all_reservations():
    """Show all reservations"""
    reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('admin/reservations.html', title='All Reservations', reservations=reservations)

@admin.route('/admin/reservations/<int:reservation_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_reservation(reservation_id):
    """Approve a reservation"""
    reservation = Reservation.query.get_or_404(reservation_id)

    # Check if the room is still available
    room = Room.query.get(reservation.room_id)
    if room.is_available(reservation.start_time, reservation.end_time):
        reservation.approve(current_user.id)
        db.session.commit()
        flash('La réservation a été approuvée !', 'success')
    else:
        flash('Impossible d\'approuver la réservation. La chambre n\'est plus disponible pendant l\'horaire demandé.', 'danger')

    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/reservations/<int:reservation_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_reservation(reservation_id):
    """Reject a reservation"""
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.reject(current_user.id)
    db.session.commit()
    flash('La réservation a été rejeté !', 'danger')
    return redirect(url_for('admin.dashboard'))
