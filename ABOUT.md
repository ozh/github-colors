# Colors of languages at GitHub

Ever wondered what colors are used for all the languages on GitHub? I did. By the way, have you seen that [awesome little rainbow](https://github.com/ozh/rainbow)?

This was inspired by [doda/github-language-colors](https://github.com/doda/github-language-colors) which was at this time a manually edited list. The thing is, their list is incomplete and sometimes colors change.

So, the idea was to automate the process and learn a little Python with a fun web-scraping exercise.

The script, `github-colors.py`, checks [Github](https://github.com/github/linguist/blob/master/lib/linguist/languages.yml) for the list of all languages, saves all colors in `colors.json` and updates the `README.md`

You can also find a version [written in Go](https://github.com/LeeReindeer/github-colors).
