# littletealeaf.github.io

[![Build Website](https://github.com/LittleTealeaf/littletealeaf.github.io/actions/workflows/build.yml/badge.svg)](https://github.com/LittleTealeaf/littletealeaf.github.io/actions/workflows/build.yml) [![CodeQL](https://github.com/LittleTealeaf/littletealeaf.github.io/actions/workflows/codeql.yml/badge.svg)](https://github.com/LittleTealeaf/littletealeaf.github.io/actions/workflows/codeql.yml)

Hi! Welcome to the repository that builds and deploys [littletealeaf.github.io](https://littletealeaf.github.io)

It's currnetly in development, so... ha!!

`Tealeaf Signing Off!`

<!-- ## The revamp

The goal of the revamp: Move away from using python AND Javascript and just using Javascript so I don't have to go back and forward and keep changin stuff

### Revamp Structure

- Use Python to setup / organize the page structure (creating a specific directory that contains a 'dynamic' based repository)
- Then, use javascript to build the pages, including fetching the API and such
- For the api in javascript, add in those extra ways we are able to use to get API endpoints -->

## Project Layout

| Folder | Usage |
| :---: | :--- |
| python | contains the python scripts |
| config | contains configuration files used in python to compile into a `generated` directory |
| *generated* | contains files generated during build time|
| *cache* | contains cache files used by any script to store files usable in future builds |
