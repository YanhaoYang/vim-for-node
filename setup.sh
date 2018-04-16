#!/bin/bash

rm -fr bundle
git clone https://github.com/VundleVim/Vundle.vim.git bundle/Vundle.vim
vim -u plugins +BundleInstall +qa
find bundle -name .git | xargs -I {} rm -fr {}
