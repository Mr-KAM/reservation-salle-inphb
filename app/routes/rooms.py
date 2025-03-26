from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.room import Room
from app.models.reservation import Reservation
from app.forms.room_forms import ReservationForm

rooms = Blueprint('rooms', __name__)

@rooms.route('/rooms')
def list_rooms():
    """List all available rooms"""
    rooms_list = Room.query.all()
    return render_template('rooms/list.html', title='Salles', rooms=rooms_list)

@rooms.route('/rooms/<int:room_id>')
def room_detail(room_id):
    """Show room details"""
    room = Room.query.get_or_404(room_id)
    # Get approved reservations for this room
    approved_reservations = Reservation.query.filter_by(
        room_id=room_id,
        status='approuvé'
    ).order_by(Reservation.start_time).all()

    return render_template(
        'rooms/detail.html',
        title=f'Room: {room.name}',
        room=room,
        reservations=approved_reservations
    )

@rooms.route('/rooms/<int:room_id>/reserve', methods=['GET', 'POST'])
@login_required
def reserve_room(room_id):
    """Reserve a room"""
    room = Room.query.get_or_404(room_id)
    form = ReservationForm()

    if form.validate_on_submit():
        # Convert form data to datetime objects
        start_time = datetime.combine(form.date.data, form.start_time.data)
        end_time = datetime.combine(form.date.data, form.end_time.data)

        # Check if the room is available during the requested time
        if room.is_available(start_time, end_time):
            reservation = Reservation(
                title=form.title.data,
                description=form.description.data,
                start_time=start_time,
                end_time=end_time,
                user_id=current_user.id,
                room_id=room.id
            )
            db.session.add(reservation)
            db.session.commit()
            flash('Votre demande de réservation a bien été soumise et est en attente d\'approbation.', 'success')
            return redirect(url_for('rooms.my_reservations'))
        else:
            flash('La salle n\'est pas disponible pendant la période demandée.', 'danger')

    return render_template(
        'rooms/reserve.html',
        title=f'Reserve {room.name}',
        form=form,
        room=room
    )

@rooms.route('/my-reservations')
@login_required
def my_reservations():
    """Show user's reservations"""
    user_reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).order_by(Reservation.created_at.desc()).all()

    return render_template(
        'rooms/my_reservations.html',
        title='Mes Réservations',
        reservations=user_reservations
    )

@rooms.route('/reservations/<int:reservation_id>')
@login_required
def reservation_detail(reservation_id):
    """Show reservation details"""
    reservation = Reservation.query.get_or_404(reservation_id)

    # Check if the user is the owner of the reservation or an admin
    if reservation.user_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'avez pas la permission de voir cette réservation.', 'danger')
        return redirect(url_for('rooms.my_reservations'))

    return render_template(
        'rooms/reservation_detail.html',
        title=f'Reservation: {reservation.title}',
        reservation=reservation
    )
