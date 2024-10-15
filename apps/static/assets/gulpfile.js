var gulp = require("gulp");
var sass = require("gulp-sass")(require("sass"));
var sourcemaps = require("gulp-sourcemaps");
var autoprefixer = require("gulp-autoprefixer");
var cleanCss = require("gulp-clean-css");
var rename = require("gulp-rename");
var browserSync = require("browser-sync").create();
const npmDist = require("gulp-npm-dist");
var wait = require("gulp-wait");

// Define COMMON paths
const paths = {
  src: {
    base: "./",
    css: "./css",
    scss: "./scss",
    node_modules: "./node_modules/",
    vendor: "./vendor",
  },
};

// Compile SCSS
gulp.task("scss", function () {
  return gulp
    .src([paths.src.scss + "/material-dashboard.scss"])
    .pipe(wait(500))
    .pipe(sourcemaps.init())
    .pipe(sass().on("error", sass.logError))
    .pipe(
      autoprefixer({
        overrideBrowserslist: ["> 1%"],
      })
    )
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(paths.src.css))
    .pipe(browserSync.stream()); // Inject CSS changes without a full reload
});

// Minify CSS
gulp.task("minify:css", function () {
  return gulp
    .src([paths.src.css + "/material-dashboard.css"])
    .pipe(cleanCss())
    .pipe(
      rename(function (path) {
        path.extname = ".min.css";
      })
    )
    .pipe(gulp.dest(paths.src.css));
});

// Watch SCSS and reload browser (for development only)
gulp.task("watch", function () {
  browserSync.init({
    server: {
      baseDir: paths.src.base, // Serve files from the base directory
    },
  });

  gulp.watch(paths.src.scss + "/**/*.scss", gulp.series("scss", "minify:css"));
  gulp.watch(paths.src.base + "/*.html").on("change", browserSync.reload);
  gulp.watch(paths.src.base + "/js/**/*.js").on("change", browserSync.reload);
});

// Development task: Includes watching and live-reloading
gulp.task("dev", gulp.series("scss", "minify:css", "watch"));

// Production task: No watching, only compiling and minifying
gulp.task("build", gulp.series("scss", "minify:css"));

