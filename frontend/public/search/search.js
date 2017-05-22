'use strict'

angular.module('doraFrontend.search', ['ngRoute'])

.config([
  '$routeProvider',
  function ($routeProvider, GoogleMapApiProviders) {
    $routeProvider.when('/host/:query*', {
      templateUrl: 'search/host.html',
      controller: 'SearchByHostCtrl'
    })
    $routeProvider.when('/search/port/:proto/:port*', {
      templateUrl: 'search/host.html',
      controller: 'SearchByPortCtrl'
    })
    $routeProvider.when('/search/:query*', {
      templateUrl: 'search/search.html',
      controller: 'SearchByKeywordCtrl'
    })
  }
])

.controller('SearchByHostCtrl', ['$scope', '$route', '$routeParams', '$http',
  function ($scope, $route, $routeParams, $http) {
    $scope.keyword = $routeParams.query

    $http.get('http://localhost:9200/dora/host/_search?q=addresses.ipv4:' + $routeParams.query + '&size=50').then(function (response) {
      console.log('API /dora/host/_search?q=addresses.ipv4', response)
      $scope.currentServices = response.data.hits.hits
    })

    $http.get('https://ipinfo.io/' + $routeParams.query).then(function (response) {
      $scope.hostGeodata = response.data
    })

    $http.get('https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&url=http://' + $routeParams.query).then(function (response) {
      var base = response.data.screenshot.data
      $scope.base64screenshot = 'data:image/jpg;base64,' + base.replace(/_/g, '/').replace(/-/g, '+')
    })
  }
])

.controller('SearchByKeywordCtrl', ['$scope', '$route', '$routeParams', '$http', '$location', 'uiGmapGoogleMapApi',
  function ($scope, $route, $routeParams, $http, $location, uiGmapGoogleMapApi) {
    $scope.keyword = $routeParams.query
    $scope.currentServices = {}
    $scope.go = function (path) {
      $location.path(path)
    }

    $http.get('http://localhost:9200/dora/host/_search?q=' + $routeParams.query + '&size=50').then(function (response) {
      console.log('API /dora/host/_search', response)
      $scope.currentServices = response.data.hits.hits
      $scope.totalFound = response.data.hits.total

      $scope.mapMarkers = []

      angular.forEach($scope.currentServices, function (value, key) {
        try {
          $scope.mapMarkers.push({
            position: {
              latitude: value._source.geo.location.latitude,
              longitude: value._source.geo.location.longitude
            },
            title: value._source.addresses.ipv4,
            icon: 'assets/images/icon-server-small.png'
          })
        } catch (e) {

        }
      })

      uiGmapGoogleMapApi.then(function (maps) {
            // Configuration needed to display the road-map with traffic
            // Displaying Ile-de-france (Paris neighbourhood)
        maps.visualRefresh = true

        $scope.map = {
          center: {
            latitude: $scope.currentServices[0]._source.geo.location.latitude,
            longitude: $scope.currentServices[0]._source.geo.location.longitude
          },
          zoom: 8,
          options: {
            mapTypeId: google.maps.MapTypeId.ROADMAP, // This is an example of a variable that cannot be placed outside of uiGmapGooogleMapApi without forcing of calling ( like ugly people ) the google.map helper outside of the function
            streetViewControl: false,
            mapTypeControl: false,
            scaleControl: false,
            rotateControl: false,
            zoomControl: false
          },
          showTraficLayer: true
        }

        console.log($scope.map)
        $scope.isOffline = false
      })
    })
  }
])

.controller('SearchByPortCtrl', ['$scope', '$route', '$routeParams', '$http',
  function ($scope, $route, $routeParams, $http) {
    $scope.keyword = $routeParams.proto + ' ' + $routeParams.port
    $scope.currentServices = {}

    $http.get('http://localhost:9200/dora/host/_search?q=services.proto:' + $routeParams.proto + ';services.port:' + $routeParams.port + '&size=50').then(function (response) {
      console.log('API /dora/host/_search', response)
      $scope.currentServices = response.data.hits.hits
    })
  }
])
