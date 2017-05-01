// Your JavaScript Code here
var app = angular.module('myApp',[]);

app.controller('thumbsnails', function($scope,$http){
    
    $http.post("/api/thumbnail").then(function(response){
        console.log(data);
        $scope.urls = response.data.thumbnails;
        
    });
});


