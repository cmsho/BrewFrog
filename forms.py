# Colton Shoenberger, cs3585@drexel.edu
# CS530: DUI, Final Project

from wtforms import Form, IntegerField, SubmitField, validators

# Filters
class Filters(Form):
    abvMin = IntegerField('Minimum: ', [validators.NumberRange(min=0, max=30)], default=0)
    abvMax = IntegerField('Maximum: ', [validators.NumberRange(min=0, max=30)], default=30)
    ibuMin = IntegerField('Minimum: ', [validators.NumberRange(min=0, max=120)], default=0)
    ibuMax = IntegerField('Maximum: ', [validators.NumberRange(min=0, max=120)], default=120)
    calMin = IntegerField('Minimum: ', [validators.NumberRange(min=0, max=400)], default=0)
    calMax = IntegerField('Maximum: ', [validators.NumberRange(min=0, max=400)], default=400)
    # submit = SubmitField('Submit')