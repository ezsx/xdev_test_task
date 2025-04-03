#!/bin/bash

# Запуск тестов после готовности сервисов
sleep 30
echo "Starting tests..."
if python3 /opt/tests/functional/test_scenario.py; then
  echo "All tests passed successfully."
else
  echo "Some tests failed. Check the logs for details."
  echo "sleep infinity for start debug tests ..."
  sleep infinity
  echo "sleep infinity doesnt work? "
  # exit 1
fi
