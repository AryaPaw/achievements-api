#!/usr/bin/env bash

# Проверяем, доступен ли FastAPI сервер
curl -f http://localhost:8000/health || exit 1

exit 0