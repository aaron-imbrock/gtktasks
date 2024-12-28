#!/usr/bin/env bash

cd ..

uv build
rm -rf build

pipx install --force dist/tasks-0.*.whl
