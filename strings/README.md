UTF-16 encoding support is not perfect, very often random bytes are treated as valid UTF-16 strings (usually Chinese). Maybe I'll come back to this someday...

### Support for checking whether a word comes from English or Polish..

We need to install dictionaries of the selected languages. The files from the apt packages will go to `/usr/share/dict`
```
sudo apt-get update
sudo apt-get install wamerican wpolish
```

The system files are large, especially for Polish, so you can alternatively download smaller ones. Sample lists can be found in this repository:

https://github.com/kkrypt0nn/wordlists
