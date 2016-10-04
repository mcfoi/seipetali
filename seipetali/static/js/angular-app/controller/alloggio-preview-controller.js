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
        .controller('alloggioPreviewCtrl', ['$scope', '$location', '$window', 'alloggioReservationServices','$filter',
            function ($scope, $location, $window, alloggioReservationServices,$filter) {
                $scope.datepicker = {}
                $scope.datepicker.format = "dd MMMM yyyy"
                $scope.datepicker.options = {
                    formatYear: 'yy',
                    startingDay: 1
                }

                $scope.$watch('alloggio_id', function (newValue, oldValue) {
                    if ($scope.alloggio_id){
                        alloggioReservationServices.setAlloggioId($scope.alloggio_id)
//                        alloggioReservationServices.getQuote();
                    }
                })

                $scope.$watch('alloggio', function (newValue, oldValue) {
                    console.log('watch alloggio:',newValue,oldValue)
                    console.log('scope.allogio:',$scope.alloggio)

                    if ($scope.alloggio){
                        alloggioReservationServices.setAlloggio($scope.alloggio)
                        alloggioReservationServices.getQuote();
                    }
                })


                $scope.parseFilterFromLocation = function(){
                     $scope.filters = {
                        checkin:{
                            date: ($location.search().checkin) ?
                                moment($location.search().checkin).toDate()
                                : null
                        },
                        checkout:{
                             date: ($location.search().checkout) ?
                                 moment($location.search().checkout).toDate()
                                 : null
                        },
                        numero_ospiti: ($location.search().numero_ospiti) ? parseInt($location.search().numero_ospiti) : null
                    }
                }
                $scope.parseFilterFromLocation()


                $scope.updateQuote = function(){
                    alloggioReservationServices.getQuote();
                }

                $scope.reservation = alloggioReservationServices.reservation
                alloggioReservationServices.filters = $scope.filters;

                $scope.requestBooking = function () {
                    alloggioReservationServices.requestBooking();
                }


                $scope.openDatepicker = function ($event, ref) {
                    $event.preventDefault();
                    $event.stopPropagation();
                    if (ref == 'in') {
                        $scope.filters.checkin.open = true;

                    } else if (ref == 'out') {
                        $scope.filters.checkout.open = true;
                    }
                }


                $scope.$watch('filters.checkin.date', function (newValue, oldValue) {
                    if (newValue === oldValue) {
                        return;
                    }
//                    console.log('update filters.checkin.date', newValue, oldValue)
                    if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date) {
                        $location.search('checkin', $filter('date')($scope.filters.checkin.date, "yyyy-MM-dd HH:mm"));

                        if (moment($scope.filters.checkin.date).add(7, 'days').toDate() > $scope.filters.checkout.date) {
                                    $scope.filters.checkout.date = moment($scope.filters.checkin.date).add(7, 'days').toDate();
                                    return;
                                }

                        if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date)
                            alloggioReservationServices.getQuote();
                    }
                })
                $scope.$watch('filters.checkout.date', function (newValue, oldValue) {
                    if (newValue === oldValue) {
                        return;
                    }
//                    console.log('update filters.checkout.date', newValue, oldValue)
                    if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date) {
                        $location.search('checkout', $filter('date')($scope.filters.checkout.date, "yyyy-MM-dd HH:mm"));

                        if (moment($scope.filters.checkout.date).subtract(7, 'days').toDate() < $scope.filters.checkin.date) {
                                    $scope.filters.checkin.date = moment($scope.filters.checkout.date).subtract(7, 'days').toDate();
                                    return;
                                }

                        if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date)
                            alloggioReservationServices.getQuote();
                    }
                })
                $scope.$watch('filters.numero_ospiti', function (newValue, oldValue) {
                    if (newValue === oldValue) {
                        return;
                    }
//                    console.log('update filters.numero_ospiti', newValue, oldValue)
                    if ($scope.filters && $scope.filters.numero_ospiti) {
                        $location.search('numero_ospiti', $scope.filters.numero_ospiti);
                        alloggioReservationServices.getQuote();
                    }
                })



//                    $scope.reservationManager  =     alloggioReservationServices()
//                    $scope.$watch(function() {
//                        return $location.path();
//                     }, function(newVal,oldVal  ){
//                       console.log('HtmlCtrl -- change location path!!!',oldVal,newVal)
//                        if(oldVal != newVal)
////                                $location.update($location.path())
////                            $window.location.href = newVal;
//                            $window.location.href = $location.url();
//                     });


//                     $scope.$watch(function(){ return $location.search() }, function(params){
//                        console.log('Update location search',params);
////                         $scope.parseFilterFromLocation()
////                                $scope.updateSearch();
////                                if (moment($location.search().checkout).toDate() != $scope.filters.checkout.date)
////                                    $scope.filters.checkout.date = moment($location.search().checkout).toDate();
//                    });

            }]);

})();