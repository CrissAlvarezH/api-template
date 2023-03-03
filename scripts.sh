#!/bin/bash

action=$1

if [ $action = "dev" ]; then
  uvicorn app.main:app --reload
fi