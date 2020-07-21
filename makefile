SHELL := /bin/bash

include .environment
export

install:
	pip install -r requirements.txt 


run:
	@echo ""
	@echo $(shell cat .environment)
	@echo ""

	uvicorn main:app --reload