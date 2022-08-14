## Project layout
All the files included in the project:

    mkdocs.yml                  # Configuration file for mkdocs.
    main.py                     # Main module which includes all the endpoints.
    db.py                       # Configuration file user for creating a database session.
    alembic.ini                 # Alembic config file when initializing
    poetry.lock                 # File with all Poetry dependencies that are needed
    pyproject.toml              # File with all necessary info about the project
    README.md                   # A usual README file
    .pre-commit-config.yaml      # File with all pre commit hooks
    auth/
        deps.py                 # File with dependencies needed for user auth.
        utils.py                # Includes reusable functions to help with user login
    crud/
        room_utils.py           # Includes CRUD functions for data associated with rooms
        booking_utils           # Includes CRUD functions for data associated with bookings
        ...                     # Other files with CRUD logic
    docs/
        index.md                # The documentation homepage.
        ...                     # Other markdown pages, images and other files.
    migrations/
        versions/               # Folder with all alembic migrations
            ...                 # Alembic version files
        env.py                  # Configuration file for Alembic
    models/
        booking.py              # Represents a model for db table Booking
        ...                     # Other files that represent models for the tables
    routers/
        room_routers.py         # Stores all the endpoints for interactions with Room
        ...                     # Other files with all the endpoints
    schemas/
        booking_schemas         # Pydantic schemas for correct response models in endpoints
        ...                     # Other files with Pydantic schemas
    tests/
        test_auth.py            # File for testing user auth
        ...                     # Other files that test the app behavior on endpoints
