'use strict';

var gulp = require('gulp');

var plugins = require('gulp-load-plugins')({
    pattern: ['gulp-*','vinyl-paths', 'del', 'browser-sync', 'stream-series'],
    replaceString: /\bgulp[\-.]/
});

const paths = {
    app:'static/',
    templates : 'templates/',
    build : 'dist/',
    delivery: 'delivery/',
    modules:[
        'jquery/dist/jquery.js',
        'underscore/underscore.js',
        'bootstrap/dist/js/bootstrap.js',
        'angular/angular.js',
        'angular-route/angular-route.js',
        'angular-resource/angular-resource.js',
        'angular-cookies/angular-cookies.js',
        'angular-animate/angular-animate.js',
        'angular-messages/angular-messages.min.js',
        'angular-bootstrap/ui-bootstrap-tpls.js',
        'angular-ui-router/release/angular-ui-router.js',
        'angular-translate/dist/angular-translate.js',
        'angular-translate-loader-static-files/angular-translate-loader-static-files.js',
        'angular-translate-storage-cookie/angular-translate-storage-cookie.js',
        'angular-strap/dist/angular-strap.js',
        'angular-strap/dist/angular-strap.tpl.js',
        'angularjs-toaster/toaster.js',
        'ng-table/dist/ng-table.js',
        'select2/select2.js',
        'angular-ui-select/select.js',
        'switchery/standalone/switchery.js',
        'ng-switchery/dist/ng-switchery.js',
        'ng-storage/ngStorage.min.js'
    ],
    cssModules:[
        'bootstrap/dist/css/bootstrap.css',
        'ng-table/dist/ng-table.css',
        'select2/select2.css',
        'angular-ui-select/select.css',
        'selectize/dist/css/selectize.default.css',
        'angular-motion/dist/angular-motion.css',
        'switchery/standalone/switchery.css',
        'angularjs-toaster/toaster.css'
    ]

};

gulp.task('webServer', function() {

    plugins.browserSync({
        notify: false,
        server: {
            baseDir: paths.build,
            middleware: function (req, res, next) {
                res.setHeader('Access-Control-Allow-Origin', '*');
                res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
                res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT');
                next();
            }}
     });
     gulp.watch(['templates/*', 'static/**/*'], ['inject', plugins.browserSync.reload]);
});

gulp.task('inject', function () {
    // Js
    var appStream = gulp.src([paths.app + 'app/moon.module.js', paths.app + 'app/moon.constants.js', paths.app + 'app/**/*.js*'])
        .pipe(plugins.concat('app.js'))
        .pipe(plugins.uglify())
        .pipe(gulp.dest(paths.build + 'js/'));

    // Modules js
    var moduleJsStream = gulp.src(paths.modules.map( function(item){return 'node_modules/' + item;}))
        .pipe(plugins.concat('modules.js'))
        .pipe(plugins.uglify())
        .pipe(gulp.dest(paths.build + 'js/'));

    //Version
    gulp.src([paths.app + '/version.json'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.build));


    // Html
    gulp.src([paths.app + 'app/**/*.html'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.build + 'html'));

    // Styles
    var cssStream = gulp.src(paths.cssModules.map( function(item){return  'node_modules/' + item;}).concat([paths.app + 'styles/main.css']))
        .pipe(plugins.concat('main.css'))
        .pipe(plugins.cleanCss())
        .pipe(gulp.dest(paths.build + 'assets/css'));

    // fonts
    gulp.src(['node_modules/bootstrap/dist/fonts/gly*'])
        .pipe(gulp.dest(paths.build + 'assets/fonts'));

    // i18n
    gulp.src([paths.app + 'i18n/*.json'])
        .pipe(gulp.dest(paths.build + 'assets/i18n'));

    // Images
    gulp.src([paths.app + 'img/*.gif', paths.app + 'img/*.png', paths.app + 'img/*.jpg'])
        .pipe(gulp.dest(paths.build + 'assets/img'));

    // Favicon
    gulp.src([paths.app + '*.ico'])
        .pipe(gulp.dest(paths.build + 'assets/img'));

    gulp.src(paths.templates + 'index.html')
        .pipe(plugins.inject(plugins.streamSeries(moduleJsStream, appStream), { ignorePath: paths.build, addRootSlash: false }))
        .pipe(plugins.inject(cssStream , { ignorePath: paths.build, addRootSlash: false }))
        .pipe(gulp.dest(paths.build));
});

gulp.task('copyMinifyHtml',function(){
    // app
    gulp.src([paths.app + 'app/**/*.html'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.build + 'html'));
});



gulp.task('webServerDelivery', function() {

    plugins.browserSync({
        notify: false,
        server: {
            baseDir: paths.delivery,
            middleware: function (req, res, next) {
                res.setHeader('Access-Control-Allow-Origin', '*');
                res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
                res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT');
                next();
            }}
    });

});

gulp.task('injectDelivery', function () {
    // Js
    var appStream = gulp.src([paths.app + 'app/moon.module.js', paths.app + 'app/moon.constants.js', paths.app + 'app/**/*.js*'])
        .pipe(plugins.concat('app.js'))
        .pipe(plugins.uglify())
        .pipe(gulp.dest(paths.delivery + 'js/'));

    // Modules js
    var moduleJsStream = gulp.src(paths.modules.map( function(item){return 'node_modules/' + item;}))
        .pipe(plugins.concat('modules.js'))
        .pipe(plugins.uglify())
        .pipe(gulp.dest(paths.delivery + 'js/'));

    //Version
    gulp.src([paths.app + '/version.json'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.delivery));


    // Html
    gulp.src([paths.app + 'app/**/*.html'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.delivery + 'html'));


    // Styles
    var cssStream = gulp.src(paths.cssModules.map( function(item){return  'node_modules/' + item;}).concat([paths.app + 'styles/main.css']))
        .pipe(plugins.concat('main.css'))
        .pipe(plugins.cleanCss())
        .pipe(gulp.dest(paths.delivery + 'assets/css'));

    // fonts
    gulp.src(['node_modules/bootstrap/dist/fonts/gly*'])
        .pipe(gulp.dest(paths.delivery + 'assets/fonts'));


    // i18n
    gulp.src([paths.app + 'i18n/*.json'])
        .pipe(gulp.dest(paths.delivery + 'assets/i18n'));

    // Images
    gulp.src([paths.app + 'img/*.gif', paths.app + 'img/*.png', paths.app + 'img/*.jpg'])
        .pipe(gulp.dest(paths.delivery + 'assets/img'));

    // Favicon
    gulp.src([paths.app + '*.ico'])
        .pipe(gulp.dest(paths.delivery + 'assets/img'));

    gulp.src(paths.templates + 'index.html')
        .pipe(plugins.inject(plugins.streamSeries(moduleJsStream, appStream), { ignorePath: paths.delivery, addRootSlash: false }))
        .pipe(plugins.inject(cssStream , { ignorePath: paths.delivery, addRootSlash: false }))
        .pipe(gulp.dest(paths.delivery));
});

gulp.task('copyMinifyHtmlDelivery',function(){
    // app
    gulp.src([paths.app + 'app/**/*.html'])
        .pipe(plugins.htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest(paths.delivery + 'html'));
});




gulp.task('build', [ 'inject', 'copyMinifyHtml']);
gulp.task('delivery', [ 'injectDelivery', 'copyMinifyHtmlDelivery']);
gulp.task('html', ['copyAndMinifyHtml']);
gulp.task('default', ['build', 'webServer' ]);