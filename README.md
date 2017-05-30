# 👋🏼 emogee <a href="https://circleci.com/gh/appointer/emogee"><img src="https://circleci.com/gh/appointer/emogee.svg?style=svg" alt="Build Status"></a>

This is an experimental CSS library which maps all emojis listed on **unicode.org**.

### Example

```html
<!-- simple hourglass emoji -->
<span class="emoji emoji-hourglass"> <!-- outputs: ⌛ -->

<!-- wow, that worked well, thumbs up -->
<span class="emoji emoji-thumbs-up-medium-dark-skin-tone"> <!-- outputs: 👍🏾 -->
```

### Generated source

The source files are generated from http://unicode.org/emoji/charts/emoji-list.html with the help of a python script located under `scripts` directory. The script is not very polished tbh but it gets the job done for now. 😜

### Develop

To run a completly fresh build follow these steps:

* run `npm install` (with dev dependencies)
* run `gulp`

Available gulp tasks are `generate` and `styles`.
