// Your JavaScript Code here
var app = angular.module('myApp',[]);
app.controller('thumbsnails', function($scope){
    $http.get("/api/thumbnail").then(function(response){
        $scope.urls = response.data.thumbnails});
});
