from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired

# Form for entering house features


class HouseForm(FlaskForm):
    PROPERTY_TYPES = [('APARTMENT', 'Apartment'),
                      ('CONDO', 'Condo'),
                      ('MULTI_FAMILY', 'Multi-Family'),
                      ('SINGLE_FAMILY', 'Single-Family'),
                      ('TOWNHOUSE', 'Townhouse')]

    NEIGHBORHOODS = [('Allston', 'Allston'),
                     ('Back Bay', 'Back Bay'),
                     ('Bay Village', 'Bay Village'),
                     ('Beacon Hill', 'Beacon Hill'),
                     ('Brighton', 'Brighton'),
                     ('Charlestown', 'Charlestown'),
                     ('Chinatown', 'Chinatown'),
                     ('Downtown', 'Downtown'),
                     ('Downtown Crossing', 'Downtown Crossing'),
                     ('East Boston', 'East Boston'),
                     ('Fenway', 'Fenway'),
                     ('Hyde Park', 'Hyde Park'),
                     ('Jamaica Plain', 'Jamaica Plain'),
                     ('Kenmore', 'Kenmore'),
                     ('Leather District', 'Leather District'),
                     ('Mattapan', 'Mattapan'),
                     ('Mission Hill', 'Mission Hill'),
                     ('North Dorchester', 'North Dorchester'),
                     ('North End', 'North End'),
                     ('Roslindale', 'Roslindale'),
                     ('Roxbury', 'Roxbury'),
                     ('South Boston', 'South Boston'),
                     ('South Dorchester', 'South Dorchester'),
                     ('South End', 'South End'),
                     ('West End', 'West End'),
                     ('West Roxbury', 'West Roxbury'),
                     ('Winthrop', 'Winthrop')]

    finished_sq_ft = IntegerRangeField('Square Foot', default=2500)
    lot_size = IntegerRangeField('Lot Size', default=2500)
    bedroom = StringField('Beds', validators=[DataRequired()])
    bathroom = StringField('Baths', validators=[DataRequired()])
    total_room = StringField('Total Rooms', validators=[DataRequired()])
    built_year = StringField('Year Built', validators=[DataRequired()])
    property_type = SelectField('Property Type', choices=PROPERTY_TYPES)
    neighborhood = SelectField('Neighborhood', choices=NEIGHBORHOODS)
    submit = SubmitField('Submit')
