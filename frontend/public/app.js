'use strict';

// Declare app level module which depends on views, and components
angular.module('doraFrontend', [
  'ngRoute',
  'ngAnimate',
  'doraFrontend.view1',
  'doraFrontend.view2',
  'doraFrontend.search',
  'doraFrontend.version'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  $locationProvider.hashPrefix('!');
  $routeProvider.otherwise({redirectTo: '/view1'});
}])
.filter('urlencode', function() {
  return function(input) {
    return window.encodeURIComponent(input);
  }
});
