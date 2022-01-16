from sqlalchemy.sql.expression import null
from excludarr.database import Base

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, DateTime, Boolean


series_seasons_association = Table(
    "serie_seasons",
    Base.metadata,
    Column("serie_id", Integer, ForeignKey("series.id")),
    Column("season_id", Integer, ForeignKey("seasons.id")),
)

seasons_episodes_association = Table(
    "seasons_episodes",
    Base.metadata,
    Column("season_id", Integer, ForeignKey("seasons.id")),
    Column("episode_id", Integer, ForeignKey("episodes.id")),
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=False, nullable=False)
    filesize = Column(Integer)
    release_date = Column(DateTime, nullable=True)
    monitored = Column(Boolean)
    tmdb_id = Column(String(255), unique=True, nullable=True)
    jw_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Movie {self.title}>"

    def __init__(
        self,
        id=None,
        title=None,
        filesize=None,
        release_date=None,
        monitored=None,
        tmdb_id=None,
        jw_id=None,
    ):
        self.id = id
        self.title = title
        self.filesize = filesize
        self.release_date = release_date
        self.monitored = monitored
        self.tmdb_id = tmdb_id
        self.jw_id = jw_id


class Serie(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=False, nullable=False)
    release_year = Column(Integer)
    monitored = Column(Boolean)
    ended = Column(Boolean)
    imdb_id = Column(String(255), unique=False, nullable=True)
    tvdb_id = Column(Integer, unique=False, nullable=True)
    jw_id = Column(Integer, nullable=True)

    seasons = relationship("Season", secondary=series_seasons_association)

    def __repr__(self):
        return f"<Serie {self.title}>"

    def __init__(
        self,
        id=None,
        title=None,
        release_year=None,
        monitored=None,
        ended=None,
        imdb_id=None,
        tvdb_id=None,
        jw_id=None,
    ):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.monitored = monitored
        self.ended = ended
        self.imdb_id = imdb_id
        self.tvdb_id = tvdb_id
        self.ended = ended
        self.jw_id = jw_id


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    season_number = Column(Integer)
    title = Column(String(255), unique=False, nullable=False)
    jw_id = Column(Integer)
    monitored = Column(Boolean)

    episodes = relationship("Episode", secondary=seasons_episodes_association)

    def __repr__(self):
        return f"<Season {self.title}>"


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True)
    episode_number = Column(Integer)
    title = Column(String(255), unique=False, nullable=False)
    jw_id = Column(Integer)
    monitored = Column(Boolean)

    def __repr__(self):
        return f"<Episode {self.title}>"
