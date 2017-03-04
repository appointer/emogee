var gulp = require('gulp');
var sass = require('gulp-sass');
var exec = require('child_process').exec;

gulp.task('generate', function(cb) {
    exec('python scripts/generate.py', function (err, stdout, stderr) {
        cb(err);
    });
});

gulp.task('styles', function() {
    gulp.src('sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./dist/'));
});

gulp.task('default', ['generate'], function () {
  gulp.start('styles');
});
