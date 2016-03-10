'use strict';
/*global app:true*/
app.controller('IndexCtrl',['$scope','$http','$routeParams','$modal', 'ENDPOINT', function ($scope, $http,$routeParams,$modal, ENDPOINT){
	$scope.current_course = $routeParams.course;
	$scope.assignmentsRequest = $http({method:'GET', url:ENDPOINT.URL+'assignments?course='+ $scope.current_course}).
		success(function(data, status, headers, config) {
		   $scope.assignments = data;
		 }).
		 error(function(data, status, headers, config) {
		 });
	$scope.showRubric = function(rubric_settings,rubric){
		var modal = $modal({title: rubric_settings.title, show:false, contentTemplate: '/views/modal_templates/rubric_template.html'});
		modal.$scope.rubric = rubric;
		modal.$scope.totalPoints = rubric_settings.points_possible;
		modal.$promise.then(modal.show);
	}

}]);