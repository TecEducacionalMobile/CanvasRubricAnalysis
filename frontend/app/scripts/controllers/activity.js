'use strict';
/*global app:true*/
app.controller('ActivityCtrl',['$scope','$http','$routeParams','$q', '$location','$rootScope','$modal','ENDPOINT', function ($scope, $http,$routeParams,$q, $location, $rootScope,$modal, ENDPOINT){
	$rootScope.log = function(variable) {
		console.log(variable);
	};
	$rootScope.alert = function(text) {
		alert(text);
	};
	$scope.changeSection = function(section){
		$scope.activeSection = section.name;
		if(section.sis_section_id == null){
			section = "";
		}
		else{
			section = section.id;
		}
		$scope.submissionsRequest = $http({method:'GET', url:ENDPOINT.URL+'assignments/'+$scope.current_course+'/'+$routeParams.assignment+'/submissions?section='+section}).
			success(function(data, status, headers, config) {
			   $scope.submissions = data;
			   for(var i = 0; i < $scope.assignment.rubric.length; i++){
			   	console.log($("#chartDiv"+$scope.assignment.rubric[i].id).html);
			   	var chart = AmCharts.makeChart("chartDiv"+$scope.assignment.rubric[i].id, {
			   	    "type": "serial",
			   	    "theme": "none",
			   	    "dataProvider": $scope.submissions[$scope.assignment.rubric[i].id],
			   	    "valueAxes": [{
			   	        			        "gridColor":"#428bca",
			   	        			        "minimum": 0,
			   	                      "max": 100,
			   	                      "maximum": 100,
			   	                      "precision": 1,
			   	                      "offset": 0,
			   	                      "title": "%",
			   	                      "titleFontSize": 10,
			   	        					"gridAlpha": 0.2,
			   	        					"dashLength": 0
			   	    }],
			   	    "gridAboveGraphs": true,
			   	    "startDuration": 1,
			   	    "graphs": [{
			   	        "balloonFunction": $scope.toolTipHelper(i),
			   	        "fillAlphas": 0.8,
			   	        "lineAlpha": 0.2,
			   	        "type": "column",
			   	        "valueField": "count"		
			   	    }],
			   	    "balloon": {
			   	    	"maxWidth": 300
			   	    },
			   	    "categoryField": "rating",
			   	    "categoryAxis": {
			   	        "gridPosition": "start",
			   	        "gridAlpha": 0,
			   	         "tickPosition":"start",
			   	         "tickLength":20
			   	    },
			   		"exportConfig":{
			   		  "menuTop": 0,
			   		  "menuItems": [{
			   	      "icon": '/lib/3/images/export.png',
			   	      "format": 'png'	  
			   	      }]  
			   		}
			   	});
			   chart.addListener("clickGraphItem", $scope.handleClick($scope.assignment.rubric[i].id));
			   }
			 }).
			 error(function(data, status, headers, config) {
			 });

	}
	$scope.activeSection = 'Todos';
	$scope.current_course = $routeParams.course;
	$rootScope.go = function(path) {
	    console.log('setting location myself to ' + path);
	    $location.path(path);
	}
	
	$scope.assignment = $routeParams.assignment;
	var assignmentDetails = $http({method:'GET', url:ENDPOINT.URL+'assignments/'+$scope.current_course+'/'+$scope.assignment}).
		success(function(data, status, headers, config) {
		   $scope.assignment = data;
		   // console.log($scope.assignment);
		 }).
		 error(function(data, status, headers, config) {
		 });
	$scope.submissionsRequest = $http({method:'GET', url:ENDPOINT.URL+'assignments/'+$scope.current_course+'/'+$scope.assignment+'/submissions'}).
		success(function(data, status, headers, config) {
		   $scope.submissions = data;
		 }).
		 error(function(data, status, headers, config) {
		 });
	$http({method:'GET', url:ENDPOINT.URL+'students/'+$scope.current_course}).
		success(function(data, status, headers, config) {
		   $scope.courseStudents = data;
		 }).
		 error(function(data, status, headers, config) {
		 });
	$http({method:'GET', url:ENDPOINT.URL+'sections/'+$scope.current_course}).
		success(function(data, status, headers, config) {
		   $scope.sections = data;
		 }).
		 error(function(data, status, headers, config) {
		 });
	

	$scope.handleClick = function(i){
		return function(event){
			$scope.activeStudents = $.grep($scope.courseStudents, function(e){ console.log(e.id); return $scope.submissions[i][event.index].students.indexOf(e.id)>-1});
			$modal({title: 'Alunos',scope: $scope, template: '/views/modal_templates/student_names.html', show: true});

		}
		
	}
	$q.all([$scope.submissionsRequest,assignmentDetails]).then(function(results){
		console.log($scope.submissions);
		console.log($scope.assignment);
		// $scope.$apply();
	
		// console.log($scope.assignment.rubric[0]);
		$scope.toolTipHelper = function(index,graph){
			return function(graphDataItem){
				var item = $.grep($scope.assignment.rubric[index].ratings, function(e){ return e.points === graphDataItem.dataContext.rating; });
				return '<b>' + graphDataItem.dataContext.rating +': </b> '+item[0].description;

			}
			
			// return graphDataItem.dataContext;

		}
		for(var i = 0; i < $scope.assignment.rubric.length; i++){
			console.log($("#chartDiv"+$scope.assignment.rubric[i].id).html);
			var chart = AmCharts.makeChart("chartDiv"+$scope.assignment.rubric[i].id, {
			    "type": "serial",
			    "theme": "none",
			    "dataProvider": $scope.submissions[$scope.assignment.rubric[i].id],
			    "valueAxes": [{
			        "gridColor":"#428bca",
			        "minimum": 0,
              "max": 100,
              "maximum": 100,
              "precision": 1,
              "offset": 0,
              "title": "%",
              "titleFontSize": 10,
					"gridAlpha": 0.2,
					"dashLength": 0
			    }],
			    "gridAboveGraphs": true,
			    "startDuration": 1,
			    "graphs": [{
			        "balloonFunction": $scope.toolTipHelper(i),
			        "fillAlphas": 0.8,
			        "lineAlpha": 0.2,
			        "type": "column",
			        "valueField": "count"		
			    }],
			    "balloon": {
			    	"maxWidth": 300
			    },
			    "categoryField": "rating",
			    "categoryAxis": {
			        "gridPosition": "start",
			        "gridAlpha": 0,
			         "tickPosition":"start",
			         "tickLength":20
			    },
				"exportConfig":{
				  "menuTop": 0,
				  "menuItems": [{
			      "icon": '/lib/3/images/export.png',
			      "format": 'png'	  
			      }]  
				}
			});
		chart.addListener("clickGraphItem", $scope.handleClick($scope.assignment.rubric[i].id));
		}
	})

}]);