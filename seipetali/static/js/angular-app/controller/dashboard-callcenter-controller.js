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
        .controller('dashboardCallcenterCtrl', ['$scope', '$location', '$window', '$filter', 'ApiReservation', 'dialogs', 'ApiPayment','ApiUser','ApiAlloggio',
            function ($scope, $location, $window, $filter, ApiReservation, $dialogs, ApiPayment,ApiUser,ApiAlloggio) {
                $scope.datepicker = {}
                $scope.datepicker.format = "dd MMMM yyyy"
                $scope.datepicker.options = {
                    formatYear: 'yy',
                    startingDay: 1
                }


                $scope.reservations = [];
                $scope.users = [];

                $scope.selected_user = null;


                var _getUsers = function(){
                    var opt = {limit:5}
                    if ($scope.search_query){
                        opt.search = $scope.search_query
                    }
                    $scope.users = ApiUser.query(opt, function(){
                        if ($scope.users.length == 1){
                            $scope.selected_user = $scope.users[0];
                            $scope.selected_user._selected = true;

                        }else{
                            $scope.selected_user = null;
                        }
                    })
                }
                _getUsers()


                var _getReservation = function(){
                    var opt = {limit:10}
                    if ($scope.filter_by_user && $scope.selected_user){
                        opt.user = $scope.selected_user.id;
                    }
                    $scope.reservations = ApiReservation.query(opt)
                }
                _getReservation()


                $scope.$watch('selected_user',function(newValue,oldValue){
                    if (newValue == oldValue) return;
                    if ($scope.filter_by_user) {
                        _getReservation();
                    }

                    if (newValue && !newValue.alloggi){
                        console.log('get alloggi dell utente',$scope.selected_user.id)
                        var opt = {owner:$scope.selected_user.id}
                        $scope.selected_user.alloggi = ApiAlloggio.query(opt)

                    }
                })


                $scope.toggleAlloggioActive = function(alloggio){

//                    alloggio.$http({
//                        method: "PATCH",
//                        url: alloggio.resource_uri,
//                        data: {active:!alloggio.active}
//                      }).then()

                    alloggio.active = !alloggio.active
                    alloggio.patch()
                }

                $scope.$watch('filter_by_user',function(newValue,oldValue){
                    if (newValue == oldValue) return;
                    _getReservation();
                })

                $scope.$watch('search_query',function(newValue,oldValue){
                    if (newValue == oldValue) return;
                    _getUsers();
                })

                $scope.usersShowNext = function(){
                     $scope.users = ApiUser.queryURL($scope.users.meta.next)
                }
                $scope.usersShowPrevious = function(){
                     $scope.users = ApiUser.queryURL($scope.users.meta.previous)
                }


                $scope.selectUser = function(user){
                    if ($scope.selected_user && $scope.selected_user._selected){
                        $scope.selected_user._selected = false;
                        if (user == $scope.selected_user) {
                            $scope.selected_user = null;
                            return;
                        }

                    }
                    console.log('$scope.users',$scope.users)
                    $scope.selected_user = user;
                    $scope.selected_user._selected = true;
                }

                $scope.selectAlloggio = function(alloggio){
                    if ($scope.selected_alloggio && $scope.selected_alloggio._selected){
                        $scope.selected_alloggio._selected = false;
                        if (alloggio == $scope.selected_alloggio) {
                            $scope.selected_alloggio = null;
                            return;
                        }

                    }
                    $scope.selected_alloggio = alloggio;
                    $scope.selected_alloggio._selected = true;
//                    console.log('$scope.selected_alloggio',$scope.selected_alloggio)
                }


                $scope.deleteReservation = function (reservation) {
                    var dlg = $dialogs.confirm('Please Confirm', 'Sei sicuro di voler eliminare questa prenotazione?');

                    dlg.result.then(function (btn) {
                        $scope.confirmed = 'You thought this quite awesome!';
                        reservation.delete().then(function () {
                                var index = $scope.reservations.indexOf(reservation);
                                $scope.reservations.splice(index, 1);
                            }
                        );
                    }, function (btn) {
                        $scope.confirmed = 'Shame on you for not thinking this is awesome!';
                    });
                }


                $scope.deletePayment = function (payment, reservation) {

                    var dlg = $dialogs.confirm('Please Confirm', 'Sei sicuro di voler eliminare questo pagamento?');

//                    var paymentId =  reservation.payments.indexOf(payment);
                    dlg.result.then(function (btn) {
                        ApiPayment.delete(payment.id).then(function () {
//                                reservation.payments.splice(paymentId, 1);

                                var idx = $scope.reservations.indexOf(reservation)
                                $scope.reservations[idx] = reservation.get()
                            }
                        );
                    }, function (btn) {
                        $scope.confirmed = 'Shame on you for not thinking this is awesome!';
                    });
                }


                $scope.registerPayment = function (reservation, payment) {
                    payment.reservation = reservation

                    var payment = ApiPayment._create_resource(payment)

                    payment.post().success(function (response, status, headers) {
                        var idx = $scope.reservations.indexOf(reservation)
                        $scope.reservations[idx] = reservation.get()
                    });
                }


            }]);

})();