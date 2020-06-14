# Journal Reader
This is a very simple web project and also my first complete web project. It is
completely devoid of any kind of a database.

## Building
The project has been dockerized, so make sure you've got `docker` and
`docker-compose` installed. This just has two containers, a `flask` container
for both the back-end and the front-end and `nginx` container to serve the
pages. I'm no professional in using docker. I'm myself learning to use docker
through this project.

You'd like to tweak the `docker-compose.yml`file to change the location of your
journals folder. You'll find instructions inside the file stating what to change.
If you get an error about the version number, just change it to `"3"` instead.

Once done, execute:
```sh
$ docker-compose up --build
```
It'll take some time to pull the images and once it is done creating the `flask`
and `nginx` containers, you can navigate to `http://127.0.0.1:_port_/` to reach
the index page. If you didn't change the _port_ to `80` in the
`docker-compose.yml` file, use the default `5000`.

To get rid of the containers, execute:
```sh
$ docker-compose down
```

## What does it do?
It just has access to a folder full of files that end with the extension `.jrl`
and it simply reads them. If the files are encrypted, it takes a key from the
user and applies the key to decrypt them. Hence renders the file in html after
parsing it.


## The Encryption Algorithm
It doesn't care whether the key is correct or not, as an incorrect key would only
lead to another form of the same gibberish as the encrypted file. The encryption
algorithm used here maps ascii to ascii and leaves symbols unaltered and hence
can be peacefully rendered by a web browser. The algorithm used here could be
guessed by any person with experience in cryptography, hence I'll skip the name
and say that the decryption algorithm is defined in `flask/src/helpers.py`. I've
taken special precaution to make it as unreadble as possible.


## File Structure
Files have extension `.jrl` as an abbreviation of the word **journal**.

### Titles
Every file has a title which is the first line of the file. The title in a file
is indicated by preceeding it with a `# ` (notice the space) for single line
titles. For multiline titles, use `"` characters to surround it.
Examples of valid titles:
```
# Today is gay
```
```
"History has been changed"
```
```
"There is no dark side of the moon, really.
Matter of fact, it's all dark."
```

### Body
As you can see there's a little amount of markdown formatting going on. I've
mostly inherited the syntaxes from Markdown and LaTeX. The markdown parsing is
not entirely done. Hyperlinks still need to be parsed and they are modelled
after Markdown files, i.e. the square brackets follwed by parentheses thing.

## Context
I'm not a web developer. I hate JavaScript. I have been writing these journal
files since the first day of college. A bunch of them have accumulated now and
if you want to view them, well, I wrote them in `vim` and then encrypted them. So
you have to decrypt them and you get a raw version of the file to read. White
text on black. So I designed this web application just to view them with ease.
I'm myself quite comfortable typing in vim, this entire project was designed just
for the viewing pleasure, and learning as well.
