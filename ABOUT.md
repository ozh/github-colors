# Colors of programming languages at GitHub

Ever wondered what colors are used for all the programming languages on GitHub? I did. By the way, have you seen that [awesome little rainbow](https://github.com/ozh/rainbow)?

This was inspired by [doda/github-language-colors](https://github.com/doda/github-language-colors) which is (was? I think it's dead) a manually edited list. The thing is, their list is incomplete and sometimes colors change.

So, the idea was to automate the process and learn a little Python with a fun web-scraping exercise.

The script, `github-colors.py`, checks https://github.com/trending for the list of all languages. Then, language after language, it checks a couple trending repo to grab their language color. Finally, the script saves all colors in `colors.json` and updates the `README.md`

This script is my first Python exercise, all feedback I gladly welcome :)
