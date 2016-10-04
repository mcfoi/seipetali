/**
 * Created with PyCharm.
 * User: elfo
 * Date: 13/01/15
 * Time: 17:29
 * To change this template use File | Settings | File Templates.
 */



(function () {
    'use strict';

    angular.module('seipetali-app')
        .controller('htmlCtrl', ['$scope', '$location','$window',
            function ($scope, $location,$window){
                    $scope.$watch(function() {
                        return $location.path();
                     }, function(newVal,oldVal  ){
                       console.log('HtmlCtrl -- change location path!!!',oldVal,newVal)
                        if(oldVal != newVal){
                             console.log($location.url());
//                                $location.update($location.path())
//                            $window.location.href = newVal;
//                            $location.path($location.url())
                            $window.location.href = $location.url();
                        }
                     });


//                     $scope.$watch(function(){ return $location.search() }, function(params){
//                        console.log('Update location search',params);
////                         $scope.parseFilterFromLocation()
////                                $scope.updateSearch();
////                                if (moment($location.search().checkout).toDate() != $scope.filters.checkout.date)
////                                    $scope.filters.checkout.date = moment($location.search().checkout).toDate();
//                    });

            }]);

})();