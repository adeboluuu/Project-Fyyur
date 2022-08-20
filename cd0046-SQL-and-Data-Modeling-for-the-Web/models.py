# Models.
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),unique=True,nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    genres = db.Column(db.String, nullable=False)
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120),nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=False)
    seeking_talent = db.Column(db.Boolean,nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
  
    def __repr__(self):
       return f'<Venue: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, genres: {self.genres}, website: {self.website}, shows: {self.shows}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False,unique=True)
    genres = db.Column(db.String(120),nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))


    def num_upcoming_shows(self):
     return self.query.join(Show).filter_by(artist_id=self.id).filter(Show.start_time > datetime.now()).count()

    def num_past_shows(self):
     return self.query.join(Show).filter_by(artist_id=self.id).filter(Show.start_time < datetime.now()).count()

    def past_shows(self):
     return Show.get_past_by_artist(self.id)

    def __repr__(self):
     return f'<Artist: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, shows: {self.shows}>'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    
    def get_past_by_venue(cls, venue_id):    
     shows = cls.query.filter_by(venue_id=venue_id).filter(cls.start_time < datetime.now()).all()
     return [show.show_details for show in shows]

    @classmethod
    def get_past_by_artist(cls, artist_id):
      shows = cls.query.filter_by(artist_id=artist_id).filter(cls.start_time < datetime.now()).all()
      return [show.show_details for show in shows]
      
    def __repr__(self):
       return f'<Show {self.id}, date: {self.date}, artist_id: {self.artist_id}, venue_id: {self.venue_id}>'

