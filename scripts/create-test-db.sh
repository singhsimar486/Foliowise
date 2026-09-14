#!/bin/bash
# Runs once when the Postgres volume is first created. Gives pytest its own
# database so the suite's TRUNCATE between tests never touches dev data.
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-SQL
    CREATE DATABASE foliowise_test;
SQL
