'use strict';

angular.module('doraFrontend.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$route', '$http',
    function($scope, $route, $http) {
        $http.get('http://localhost:9200/dbot/host/_search?q=services.state:open&size=50').then(function(response) {
            console.log('API /dbot/host/_search?q=services.state:open', response);
            $scope.currentServices = response.data.hits.hits;
        });
    }
]);
