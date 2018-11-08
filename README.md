# TAP_tools
Tools for developing datasets for the Trajectory Analysis Planner


[Trajectory Analysis Planner (TAP)](https://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/trajectory-analysis-planner.html) is a software tool designed to help answer the crucial question in any Area Contingency Plan: How do I develop a plan that protects my area against likely oil spills?


To generate datasets for TAP, a oil spill transport model is run thousands of times to generate data that can then be analysis for statistics of oil transport.

This repository holds scripts and utilities to make run [PyGNOME](https://github.com/NOAA-ORR-ERD/PyGnome) and process the results for the TAP viewing application.

## The `tap_tools` package

The goal is to have a single `tap_tools` python package with the scripts an utilities everyone needs.

But in the meantime, each contributer can dump their code into separate directories as we work to put together the "proper" package.

## Partners

As multiple groups are using py_gnome for TAP processing, this repo can serve as a collaboration location to share scripts, tips, and techniques.

If you have something to contribute -- fork the repo, add your stuff, and make a PR to merge it into the project. If you are already working with NOAA, ask us for permissions to push directly to this repo.

