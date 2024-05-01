# reedsy-book-challenge

External Libraries used for this project apart from teh default installed with a new Vue project:
 
 - TailwindCss
 - Prettier

I set up my IDE to run Prettier on every file change, in a real project, we would check on CI that prettier style is being applied.


Note on Comments: I implemented the form logic very manually for this, I'm sure there are better ways to do it using external libraries (like Formik in React) but I thought for this simple task I didn't need to go that far.

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
