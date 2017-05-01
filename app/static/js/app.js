// Your JavaScript Code here
var app = angular.module('myApp',[]);

app.controller('thumbsnails', function($scope,$http){
    
    $http.post("/api/<int:wishid>/thumbnail").then(function(response){
        $scope.urls = response.data;
        
    });
});


