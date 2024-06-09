# Form to model utility function
from wtforms import Form, FormField, FieldList, StringField, EmailField, SubmitField, SelectField, BooleanField, IntegerField, FloatField
from wtforms.validators import InputRequired, Optional, Email
from sqlalchemy.sql.sqltypes import Integer, String, Float

satypes2form = {
  Integer:IntegerField, String:StringField, Float:FloatField
}

def model2form(model):
    from flask import current_app
    db = current_app.extensions['sqlalchemy']
    class TemplateForm(FlaskForm):
        submit = SubmitField('Submit')        
    for fk in model.__table__.foreign_keys:
        setattr(
            TemplateForm, fk.column.table.name+'_id',
            SelectField(
                fk.column.table.name,
                choices = [
                    (r.id,str(r)) for r in
                    db.Model._sa_registry._class_registry[
                        fk.column.table.name.capitalize()
                    ].query.all()
                ]
            )
        )
    for c in model.__table__.columns:
        if c.name in ('id',) or c.name.endswith('_id'): continue
        setattr(
            TemplateForm, c.name, satypes2form[type(c.type)](c.name)
        )
    return TemplateForm
