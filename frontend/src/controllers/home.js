module.exports = function($scope, $rootScope, Http) {
    $scope.books = [];
    $scope.next  = null;

    $scope.showBooks = function(t) {
        Http.sendGet(t).then(
            function(response) {
                $scope.books.push.apply($scope.books, response.data.results);
                $scope.next  = response.data.next;
            }
        );
    }
}