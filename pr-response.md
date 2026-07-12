# PR Response Doc — CineLog Watchlist Feature

## AI Usage


## Comment 1 — Rename

**What I did:**
I renamed `save_to_watchlist()` to `add_to_watchlist()` in `services/watchlist_service.py`. I also updated the import and function call in `routes/watchlist/watchlist.py`.

**How I verified:**
I searched the full repository for `save_to_watchlist` and confirmed that no references to the old name remained. I also ran the full test suite.

## Comment 2 — Deduplication

**What I did:**
Before creating a new `WatchlistEntry`, `add_to_watchlist()` now queries for an existing entry with the same `user_id` and `film_id`. If one exists, the function raises `AlreadyInWatchlistError` rather than inserting another row. I also added a database-level unique constraint for the same pair.

**How I verified:**
I added a test that adds a film to a user's watchlist and then attempts to add the same film again. The test verifies that `AlreadyInWatchlistError` is raised. The database constraint also protects against duplicates if the service-level check is bypassed.

## Comment 3 — Missing test

**What I did:**
I created `tests/test_watchlist.py` and added a test for a validly formatted UUID that does not correspond to an existing film.

**How I verified:**
The test calls `add_to_watchlist()` with `00000000-0000-0000-0000-000000000000` and verifies that `FilmNotFoundError` is raised. I modeled the test after `test_add_to_collection_nonexistent_film_raises` in `tests/test_collection.py`.

## Comment 4 — Default visibility

**My position:**
I kept `public=True` as the default for watchlist entries.

**Reasoning:**
CineLog is a community film-tracking application, so public lists support discovery and social interaction. A public default makes it easier for users to share films they plan to watch and allows other users to discover films through those lists. This is consistent with optimizing the feature for community participation rather than treating every watchlist as private personal data.

**Tradeoff acknowledged:**
A public default is less privacy-preserving because some users may not realize their saved films are visible. A private-by-default design would reduce that risk, but it would also make the community aspect of the feature less useful. A future improvement should expose visibility clearly in the API and user interface so users can explicitly choose between public and private lists.

## Comment 5 — Sort order

**My position:**
I changed the default sort order from alphabetical to newest-added-first.

**Reasoning:**
A watchlist represents a user's current intent. Films added recently are usually more relevant than films saved much earlier. Newest-first ordering also matches the existing `get_collection()` behavior, which orders collection entries by `date_added` descending. Keeping both features consistent makes the API easier to understand.

**Engagement with reviewer's point:**
I agree that users are more likely to look for something they recently saved than to browse their entire watchlist alphabetically. Alphabetical sorting remains useful for large lists, but it would be better implemented later as an explicit sorting option rather than as the default.

## Comment 6 — Rebase

**What conflicted:**
The updated `main` branch changed film identifiers from integers to UUID strings. The watchlist model and service code were still based on the earlier integer-ID implementation.

**How I resolved it:**
I rebased `feature/watchlist` onto `origin/main`. During conflict resolution, I retained the UUID implementation from `main` and updated `WatchlistEntry.user_id`, `WatchlistEntry.film_id`, service parameters, and tests to use UUID strings. Film lookup now uses `db.session.get(Film, film_id)`.

**How I verified no conflict remains:**
I ran the full test suite and checked the branch history for merge commits. I also searched the watchlist implementation to confirm that no integer film-ID declarations remained.

## PR Description

### Overview

This pull request adds a watchlist feature to CineLog. Users can add films they plan to watch and retrieve their saved watchlist through the REST API.

The implementation includes:

* A `WatchlistEntry` database model
* An `add_to_watchlist()` service function
* Duplicate-entry prevention
* Missing-film validation
* REST endpoints for adding and retrieving watchlist entries
* UUID-compatible user and film identifiers
* Automated watchlist tests

### Design decisions

Watchlists default to `public=True` because CineLog is a community film-tracking application and public lists support film discovery and sharing. The tradeoff is that public-by-default behavior is less privacy-preserving, so a future interface should make visibility explicit to users.

Watchlists are ordered by `date_added` descending. This places recently saved films first and matches the behavior of CineLog's existing collection service.

### Manual testing

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask application:

   ```bash
   python app.py
   ```

3. Add an existing film to a user's watchlist:

   ```bash
   curl -X POST \
     http://127.0.0.1:5000/watchlist/<user_id>/add \
     -H "Content-Type: application/json" \
     -d '{"film_id":"<film_uuid>"}'
   ```

4. Repeat the same request and verify that the API returns a duplicate-entry error.

5. Send a request using a nonexistent UUID and verify that the API returns a not-found error.

6. Retrieve the user's watchlist:

   ```bash
   curl http://127.0.0.1:5000/watchlist/<user_id>
   ```

7. Verify that the newest entry appears first.

8. Run the automated tests:

   ```bash
   pytest tests/ -v
   ```

## Git history screenshot

Add the `git log --oneline` screenshot here before submission.
