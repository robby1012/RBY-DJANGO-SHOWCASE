module.exports = function($scope, $window, $timeout, Http) {
    $scope.firstname = null;
    $scope.lastanme  = null;
    $scope.username  = null;
    $scope.email     = null;
    $scope.password  = null;
    $scope.password2 = null;
    $scope.error     = null;
    $scope.errors    = {}
    $scope.success   = null;
    $scope.isSubmit  = true;

    $scope.submit = function() {
        $scope.isSubmit = false;

        let data = {
            first_name: $scope.firstname,
            last_name : $scope.lastname,
            username  : $scope.username,
            email     : $scope.email,
            password  : $scope.password,
            password2 : $scope.password2
        }

        Http.sendAsJson('post', 'http://localhost:8000/api/v1/authentication/registration/', {'data': data}).then(
            function success(response) {
                $scope.error   = null;
                $scope.errors  = {}
                $scope.success = 'Your registration is success! You will be redirected soon'
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