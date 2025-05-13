// define constant value
const API = 'localhost:8000/api/v1'

require('./less/web.less');

// Angularjs require
var angular = require('angular');
require('angular-route');
require('ng-file-upload');
require('angular-sanitize');

// AngularJS module working
var app = angular.module('App', ['ngRoute', 'ngFileUpload', 'ngSanitize']);

// Register AngularJS custom factory
app.factory('Http', require('./http'));

// Configuration router
app.config(function($routeProvider) {
    $routeProvider.when(
        '/',
        {
            templateUrl: 'templates/home.html',
            controller: 'HomeController'
        },
    ).when(
        '/book/:uuid',
        {
            templateUrl: 'templates/book.html',
            controller: 'DetailController'
        },
    ).when(
        '/login',
        {
            templateUrl: 'templates/login.html',
            controller: 'LoginController'
        },
    ).when(
        '/register',
        {
            templateUrl: 'templates/register.html',
            controller: 'RegisterController'
        },
    )
});

app.controller('RootController', function($rootScope, $window, Http){
    $rootScope.auth  = null;

    Http.sendGet('http://localhost:8000/api/v1/authentication/token/', $window.localStorage.getItem('token')).then(
        function (response){
            let responseData = response.data;
            $rootScope.auth  = responseData;
        }
    )
});
app.controller('HomeController', require("./controllers/home"));
app.controller('DetailController', require("./controllers/detail"));
app.controller('RegisterController', require("./controllers/register"));
app.controller('LoginController', require("./controllers/login"));
