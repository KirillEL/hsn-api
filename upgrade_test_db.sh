#!/bin/bash

export DB_URI=$DATABASE_URL
alembic upgrade head