import pytest

from services.collection_service import FilmNotFoundError
from services.watchlist_service import (
    AlreadyInWatchlistError,
    add_to_watchlist,
)


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    fake_film_id = "00000000-0000-0000-0000-000000000000"

    with app.app_context():
        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(sample_user, fake_film_id)

def test_add_to_watchlist_duplicate_raises(
    app,
    sample_user,
    sample_film,
):
    with app.app_context():
        add_to_watchlist(sample_user, sample_film)

        with pytest.raises(AlreadyInWatchlistError):
            add_to_watchlist(sample_user, sample_film)