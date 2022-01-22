from loguru import logger
from rich.progress import Progress

from excludarr.core import RadarrActions, SonarrActions
from excludarr.database import Movie, Serie, init_db

import excludarr.utils.filters as filters


class SyncActions:
    def __init__(
        self,
        radarr,
        sonarr,
        database_path,
        locale,
        radarr_url=None,
        radarr_api_key=None,
        radarr_verify_ssl=None,
        sonarr_url=None,
        sonarr_api_key=None,
        sonarr_verify_ssl=None,
    ):
        logger.debug("Initializing database")
        self.session = init_db(database_path)

        if radarr:
            self.radarr_actions = RadarrActions(
                radarr_url, radarr_api_key, locale, radarr_verify_ssl
            )
        if sonarr:
            self.sonarr_actions = SonarrActions(
                sonarr_url, sonarr_api_key, locale, sonarr_verify_ssl
            )

    def sync_movies(self):
        # Get all movies listed in Radarr
        logger.debug("Getting all the movies from Radarr")
        radarr_movies = self.radarr_actions.get_movies()

        logger.debug("Syncing all movies to database")
        for movie in radarr_movies:
            id = movie["id"]
            title = movie["title"]
            filesize = movie["sizeOnDisk"]
            release_date = filters.get_release_date(movie)
            release_year = filters.get_string_from_datetime(release_date, "%Y")
            monitored = movie["monitored"]
            tmdb_id = movie["tmdbId"]

            db_movie = self.session.query(Movie).filter(Movie.id == id).first()
            if isinstance(db_movie, Movie):
                valid_jw_id = self.radarr_actions.validate_jw_id(title, tmdb_id, db_movie.jw_id)
                if valid_jw_id:
                    jw_id = db_movie.jw_id
                else:
                    jw_id = self.radarr_actions.get_jw_id(title, tmdb_id, release_year, True)
            else:
                jw_id = self.radarr_actions.get_jw_id(title, tmdb_id, release_year, True)

            self.session.merge(
                Movie(
                    id=id,
                    title=title,
                    filesize=filesize,
                    release_date=release_date,
                    monitored=monitored,
                    tmdb_id=tmdb_id,
                    jw_id=jw_id,
                )
            )

            self.session.commit()

    def sync_series(self):
        # Get all series listed in Sonarr
        logger.debug("Getting all the series from Sonarr")
        sonarr_series = self.sonarr_actions.get_series()

        logger.debug("Syncing all series to database")
        for serie in sonarr_series:
            id = serie["id"]
            title = serie["title"]
            release_year = int(serie["year"])
            monitored = serie["monitored"]
            imdb_id = serie.get("imdbId", None)
            tvdb_id = serie.get("tvdbId", None)
            ended = serie["ended"]

            db_serie = self.session.query(Serie).filter(Serie.id == id).first()
            # if isinstance(db_serie, Movie):
            #     valid_jw_id = self.sonarr_actions.validate_jw_id(title, tmdb_id, db_movie.jw_id)
            #     if valid_jw_id:
            #         jw_id = db_serie.jw_id
            #     else:
            #         jw_id = self.radarr_actions.get_jw_id(title, tmdb_id, release_year, True)
            # else:
            #     jw_id = self.radarr_actions.get_jw_id(title, tmdb_id, release_year, True)

            self.session.merge(
                Serie(
                    id=id,
                    title=title,
                    release_year=release_year,
                    monitored=monitored,
                    ended=ended,
                    imdb_id=imdb_id,
                    tvdb_id=tvdb_id,
                    jw_id=None,
                )
            )

            self.session.commit()
