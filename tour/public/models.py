# -*- coding: utf-8 -*-
"""Points models."""

from tour.database import Column, Model, db

categories = ['Park', 'Museum', 'Restaurant']

class Point(Model):
    """A point model of the app."""

    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(80), nullable=False)
    category = Column(db.String(80), nullable=False)
    public = Column(db.Boolean(), default=False)
    latitude = Column(db.String(15), nullable=False)
    longitude = Column(db.String(15), nullable=False)


    def __init__(self, name, category, public, latitude, longitude):
        """Create instance."""
        db.Model.__init__(self, name=name, category=category)
        
        if category not in categories:
            self.category = '--'
        else:
            self.category = category[0]

        self.name = name[0]
        self.public = public
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Point({name!r})>'.format(name=self.name)
