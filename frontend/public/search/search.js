'use strict';

angular.module('doraFrontend.search', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/host/:query*', {
        templateUrl: 'search/host.html',
        controller: 'SearchByHostCtrl'
    });
    $routeProvider.when('/search/port/:proto/:port*', {
        templateUrl: 'search/host.html',
        controller: 'SearchByPortCtrl'
    });
    $routeProvider.when('/search/:query*', {
        templateUrl: 'search/search.html',
        controller: 'SearchByKeywordCtrl'
    });
}])

.controller('SearchByHostCtrl', ['$scope', '$route', '$routeParams', '$http',
function($scope, $route, $routeParams, $http) {
    $scope.keyword = $routeParams.query;

    $http.get('http://localhost:9200/dbot/host/_search?q=addresses.ipv4:' + $routeParams.query + '&size=50').then(function(response) {
        console.log('API /dbot/host/_search?q=addresses.ipv4', response);
        $scope.currentServices = response.data.hits.hits;
    });

    $http.get('https://ipinfo.io/' + $routeParams.query).then(function(response) {
        $scope.hostGeodata = response.data
    });

    $http.get('https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&url=http://' + $routeParams.query).then(function(response) {
        var base = response.data.screenshot.data;
        $scope.base64screenshot = 'data:image/jpg;base64,' + base.replace(/_/g, '/').replace(/-/g,'+');
    });
}
])

.controller('SearchByKeywordCtrl', ['$scope', '$route', '$routeParams', '$http',
function($scope, $route, $routeParams, $http) {
    $scope.keyword = $routeParams.query;
    $scope.currentServices = {};

    $http.get('http://localhost:9200/dbot/host/_search?q=' + $routeParams.query + '&size=50').then(function(response) {
        console.log('API /dbot/host/_search', response);
        $scope.currentServices = response.data.hits.hits;
    });
}
])

.controller('SearchByPortCtrl', ['$scope', '$route', '$routeParams', '$http',
function($scope, $route, $routeParams, $http) {
    $scope.keyword = $routeParams.proto + ' ' + $routeParams.port;
    $scope.currentServices = {};

    $http.get('http://localhost:9200/dbot/host/_search?q=services.proto:' + $routeParams.proto + ';services.port:' + $routeParams.port + '&size=50').then(function(response) {
        console.log('API /dbot/host/_search', response);
        $scope.currentServices = response.data.hits.hits;
    });
}
]);
