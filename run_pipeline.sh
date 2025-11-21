#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U postgres; do
  sleep 2
done

echo "PostgreSQL is ready!"

# Run dbt pipeline
echo "Running dbt pipeline..."
docker-compose run --rm dbt dbt deps
docker-compose run --rm dbt dbt seed
docker-compose run --rm dbt dbt run
docker-compose run --rm dbt dbt test

echo "dbt pipeline completed!"
echo "Dashboard available at: http://localhost:8501"
