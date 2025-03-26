from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import datetime, time

class ReservationForm(FlaskForm):
    title = StringField('Titre de la Réservation',
                        validators=[DataRequired(), Length(min=3, max=100)])
    description  = TextAreaField('Description',
                               validators=[Length(max=500)])
    date  = DateField('Date',
                    validators=[DataRequired()],
                    format='%Y-%m-%d')
    start_time  = TimeField('Heure de Début',
                          validators=[DataRequired()],
                          format='%H:%M')
    end_time  = TimeField('Heure de Fin',
                        validators=[DataRequired()],
                        format='%H:%M')
    submit  = SubmitField('Faire une demande de réservation')


    def validate_date(self, date):
        if date.data < datetime.now().date():
            raise ValidationError('La date de réservation ne peut pas être dans le passé.')

    def validate_end_time(self, heure_fin):
        if self.start_time.data and self.end_time.data:
            if self.end_time.data <= self.start_time.data:
                raise ValidationError('L\'heure de fin doit être après l\'heure de début.')


class RoomForm(FlaskForm):
    name  = StringField('Nom de la Chambre',
                      validators=[DataRequired(), Length(min=3, max=100)])
    capacity  = IntegerField('Capacité',
                           validators=[DataRequired(), NumberRange(min=1)])
    location  = StringField('Emplacement',
                             validators=[DataRequired(), Length(min=3, max=200)])
    description  = TextAreaField('Description',
                               validators=[Length(max=500)])
    submit  = SubmitField('Ajouter une salle à la base de donnée')
