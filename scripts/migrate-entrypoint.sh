#!/bin/sh

ARGS="${@}"
if [ -z "${ARGS}" ]; then
    echo ${ARGS}
fi

migrate -path=/migrations -database=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}?sslmode=disable ${ARGS}