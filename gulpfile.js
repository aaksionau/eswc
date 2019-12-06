const gulp = require("gulp"),
  browserSync = require("browser-sync").create(),
  sass = require("gulp-sass"),
  cleanCSS = require("gulp-clean-css"),
  rename = require("gulp-rename"),
  minifyCss = require('gulp-minify-css'),
  concat = require("gulp-concat"),
  clean = require('gulp-clean'),
  autoprefixer = require('gulp-autoprefixer');

  sass.compiler = require("node-sass");

const exec = require('child_process').exec;

const compileStyle = () => {   
  return gulp.src('./static/css/all.sass')
  .pipe(sass().on("error", sass.logError))
  .pipe(autoprefixer('last 2 versions'))
  .pipe(minifyCss())
  .pipe(cleanCSS())
  .pipe(rename("style.min.css"))
  .pipe(gulp.dest('./static/css/'));
}

const watchStyle = () => {
  const watcher = gulp.watch(['./static/sass/*.sass', './**/static/sass/*.sass']);
  watcher.on('change', function(path, stats) {
    console.log(`changed file: ${path}`);
    compileStyle();
  });
}

const startServer = () => {
  exec('python manage.py runserver')
  browserSync.init({
    notify: false,
    proxy: 'http://127.0.0.1:8000'
  })
}

const compile = gulp.series(compileStyle)
const serve = gulp.series(compile, startServer)
const defaultTasks = gulp.parallel(serve, watchStyle)

exports.default = defaultTasks