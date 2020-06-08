#!/bin/bash
for filename in ./itaqa/test/test_*.py; do
    echo "Testing $filename..."
    pytest -s -v $filename
done