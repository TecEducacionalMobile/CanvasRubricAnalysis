'use strict';
/*global app:true*/
var loginRequired = function($location, $q, $rootScope) {  
    var deferred = $q.defer();

    if(!$rootScope.sessionUser) {
        deferred.reject()
        $location.path('/');
    } else {
        deferred.resolve()
    }

    return deferred.promise;
}
var app = angular.module('frontendApp', [
  'cgBusy',
  'ngCookies',
  'angular-loading-bar',
  'ngResource',
  'ngSanitize',
  'ngRoute',
  'mgcrea.ngStrap'
]);
app.config(function (cfpLoadingBarProvider, $routeProvider, $locationProvider) {
    cfpLoadingBarProvider.latencyThreshold = 10;
    $routeProvider
      .when('/course/:course',{
        templateUrl:'views/principal.html',
        controller:'IndexCtrl'})
      .when('/course/:course/assignment/:assignment',{
        templateUrl:'views/activitySummary.html',
        controller:'ActivityCtrl'})
      .otherwise({
        redirectTo: '/'
      });
    // $locationProvider.html5Mode(true);
  });
app.constant('ENDPOINT',{
  'URL': 'https://rubricamobilevirtual.appspot.com/api/'
});