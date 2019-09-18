#!/bin/bash

branch=${TRAVIS_BRANCH}
if [ ! -z "${HEAD_BRANCH}" ]; then
  branch=${HEAD_BRANCH}
fi

git checkout -f ${branch}
