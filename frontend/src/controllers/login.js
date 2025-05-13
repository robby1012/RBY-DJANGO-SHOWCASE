module.exports = function($scope, $window, $timeout, Http) {
    $scope.username  = null;
    $scope.password  = null;
    $scope.error     = null;
    $scope.errors    = {}
    $scope.success   = null;
    $scope.isSubmit  = true;

    $scope.submit = function() {
        $scope.isSubmit = false;

        let data = {
            username  : $scope.username,
            password  : $scope.password
        }

        Http.sendAsJson('post', 'http://localhost:8000/api/v1/authentication/token/', {'data': data}).then(
            function success(response) {
                $scope.error   = null;
                $scope.errors  = {};
                $scope.success = 'Your login is success! You will be redirected soon';
                $window.localStorage.setItem('token', response.data.token);
                $timeout(
                    function(){
                        $window.location.href = '/#!';
                    }, 2500
                );
            },
            function error(response) {
                let responseData = response.data;
                $scope.error  = null;
                $scope.errors = {}
                $scope.isSubmit = true;

                if('non_field_errors' in responseData){
                    $scope.error = responseData.non_field_errors[0];
                } else {
                    $scope.errors = response.data;
                }
                console.log(response)
            }
        );
    }
}