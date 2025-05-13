module.exports = function($scope, $routeParams, Http) {
    $scope.book = {}

    $scope.showBook = function(i) {
        Http.sendGet('http://localhost:8000/api/v1/library/book/' + $routeParams.uuid + '/').then(
            function(response) {
                $scope.book = response.data;
            }
        );
    }
}