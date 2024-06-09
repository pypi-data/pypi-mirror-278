# vigor

<!-- [![pypi](https://img.shields.io/pypi/v/vigor.svg)](https://pypi.python.org/pypi/vigor)
[![versions](https://img.shields.io/pypi/pyversions/vigor.svg)](https://github.com/ryanliu6/vigor) -->
[![license](https://img.shields.io/github/license/ryanliu6/vigor.svg)](https://github.com/ryanliu6/vigor/blob/main/LICENSE)

A collection of semi-random functions and scripts that I found useful for my own usage, packed into a Python library for ease-of-use.

## Scripts
Currently there are two categories of scripts, one for files and one for Git repos.

`author-rewrite.sh` script found under the Git folder was not written by me, but provided by GitHub previously for the purpose of fixing commit history. I was not able to find the same script on GitHub's official documentation and chose to preserve it in this collection.

## Docker Compose
One problem I encountered when creating [Focus](https://github.com/ryanliu6/focus) (docker containers that run on my own multi-media server), was that after separating individual services into subdirectories, generating a "main" or "aggregated" compose file was difficult with existing Docker Compose libraries. Thus, the compose module was born for the purpose of generating custom compose files based on selected services.
