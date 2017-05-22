/**
Copyright 2017 Jorge Matricali

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

'use strict'

// Declare app level module which depends on views, and components
angular.module('doraFrontend', [
  'ngRoute',
  'ngAnimate',
  'ui.bootstrap',
  'uiGmapgoogle-maps',
  'doraFrontend.view1',
  'doraFrontend.view2',
  'doraFrontend.search',
  'doraFrontend.version'
])
.config([
  '$locationProvider',
  '$routeProvider',
  'uiGmapGoogleMapApiProvider',
  function ($locationProvider, $routeProvider, GoogleMapApiProviders) {
    $locationProvider.hashPrefix('!')
    $routeProvider.otherwise({redirectTo: '/view1'})
    GoogleMapApiProviders.configure({
      v: '3.20',
      libraries: 'weather,geometry,visualization'
    })
  }
])
.filter('urlencode', function () {
  return function (input) {
    return window.encodeURIComponent(input)
  }
})
