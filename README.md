# Automata

Automata is a simple python package to automate the setup of Ubuntu machines. Automata has it's own DSL based on YAML syntax 
to specify the configuration for the Ubuntu machine. 

To run:

```
python3 main.py --file examples/lab/configuration.yml
```

## Automata DSL 

The configuration file should have following structure:

```yml
- version: '0.1'

# a function
- apt_keys:
  - https://dl.yarnpkg.com/debian/pubkey.gpg
...
```

At top you have to define the version and then following that you can specify what command you want to run 
using the functions defined in automata(e.g. `apt_keys`).

Automata will go through the configuration from top to bottom and you can also have the same function used multiple times.

Following section go through the available functions.

### apt_keys

Add a list of apt keys from a local file or from an HTTP URL. Uses `sudo`.

```
- apt_keys:
  - https://dl.yarnpkg.com/debian/pubkey.gpg
  - /home/foo/pubkey.gpg
```

### apt_packages

Install a list of apt packages. First the block will perform an `apt update` and then install the packages one at a time.
Uses `sudo`.

```
- apt_packages:
  - vim
  - nginx
```

### bash_scripts

Use `bash_scripts` function to execute a bash script in a local file or a through an HTTP(S) URL. 
Uses `bash` to run the script locally.

```
- bash_scripts:
    - https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh
    - /home/foo/myscript.sh
``` 

### sources

Use `sources` function to add a source repository file to `/etc/apt/sources.list.d` directory. 
So it will be used by apt to find packages.

```
- sources:
    # yarn.list file will be created in sources.list.d with the content
  - yarn: deb https://dl.yarnpkg.com/debian/ stable main
```

### files

To copy files from a destination to a source location. Takes a list where each list should contain `dest`, and `src` property. Optionally can set `sudo` property 
to `yes` to indicate you need to use `sudo`. `dest` and `src` are should be pointing to local files. 

```
- files:
  -
    dest: /etc/nginx/nginx.conf
    src: examples/lab/configurations/nginx.conf
    sudo: yes
```

### systemd.services

To perform particular action on `systemd` services, you can use this function. 

```
- systemd.services:
    # restart nginx service
    nginx: restart
```

### git

`git` function handles git commands. Currently only support `clone`.

```
- git:
  -
   clone: https://github.com/NirantK/awesome-project-ideas
   dest: /home/foo/temp/awesome-project-ideas
```

## Development

- Python 3
- Following Python packages:
    - yaml
    - pydevd_pycharm (for remote debugging)
