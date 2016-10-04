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
        .service('alloggioReservationServices', ['ApiAlloggio','djangoUrl','$http','$window',
            function (ApiAlloggio,djangoUrl,$http,$window) {
                console.log('Init alloggioReservationServices')
                var self = this;

                self.alloggioId = null;
                self.alloggio = null;
//                self.isAvailable = false;
                self.numero_ospiti = 0;
                self.checkin = null;
                self.checkout = null;
                self.options = [];

                self.reservation = {
                    isAvailable : false
                }
                self.filters = {};


                self.setAlloggioId = function(id){
                    console.log('setAlloggioId',id)
                    self.alloggioId = id;
                }
                self.setAlloggio = function(obj){
                    console.log('setAlloggio',obj)
                    self.alloggio = obj;
                }

                console.log(ApiAlloggio._get_detail_url(self.alloggioId));


                function getQuoteReservationData(){
                    var options = {}

                    if (self.filters && self.filters.checkout && self.filters.checkout.date)
//                                    options.end = moment(self.filters.checkout.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) .format('YYYY-MM-DD HH:mm:ss ZZ')
                        options.end = moment(self.filters.checkout.date).format('YYYY-MM-DD HH:mm:ss')

                    if (self.filters && self.filters.checkin && self.filters.checkin.date)
//                                    options.start = moment(self.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
                        options.start = moment(self.filters.checkin.date).format('YYYY-MM-DD HH:mm:ss')

                    if (self.filters && self.filters.numero_ospiti )
//                                    options.start = moment(self.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
                        options.numero_ospiti = self.filters.numero_ospiti



                    options.servizi_opzionali = [];

                    angular.forEach(self.alloggio.servizi_opzionali, function(value, key) {
//                        console.log(key + ': ' + value);
                        if (value.selected){
                            this.push(value.resource_uri);
                        }
//                        this.push('peppe');
//                          this.push(key + ': ' + value);

                    }, options.servizi_opzionali);

                    return options;
                }

                self.getQuote = function(){
//                    Richiede la quotazione secondo i parametri indicati e verifica la disponibilita
                        var url = djangoUrl.reverse('api_alloggio_quote',{api_name:'v1',resource_name:'alloggio',pk:self.alloggioId})
                        console.log('verifyAvailability',url)
                        
                        var options = getQuoteReservationData();

//                        if (self.filters && self.filters.checkout && self.filters.checkout.date)
////                                    options.end = moment(self.filters.checkout.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) .format('YYYY-MM-DD HH:mm:ss ZZ')
//                            options.end = moment(self.filters.checkout.date).format('YYYY-MM-DD HH:mm:ss')
//
//                        if (self.filters && self.filters.checkin && self.filters.checkin.date)
////                                    options.start = moment(self.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
//                            options.start = moment(self.filters.checkin.date).format('YYYY-MM-DD HH:mm:ss')
//
//                        if (self.filters && self.filters.numero_ospiti )
////                                    options.start = moment(self.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
//                            options.numero_ospiti = self.filters.numero_ospiti
//
//
//
//                        options.servizi_opzionali = [];
//
//                        angular.forEach(self.alloggio.servizi_opzionali, function(value, key) {
//                            console.log(key + ': ' + value);
//                            if (value.selected){
//                                this.push(value.resource_uri);
//                            }
//                            this.push('peppe');
////                          this.push(key + ': ' + value);
//
//                        }, options.servizi_opzionali);

                        if (options.start && options.end && options.numero_ospiti){
                            console.log('options:',options)

                            $http({
                                method: 'GET',
                                url: url,
                                params: options
                            }).success(function (result) {
                                    self.reservation.isAvailable = true;
//                                    self.reservation.total = result.total;
//                                    self.reservation.caparra = result.caparra;
                                    self.reservation.quote = result
                                   console.log(result)
                            }).error(function(result){
                                    console.log('error:',result)
                                    self.reservation.isAvailable = false;
                                    self.reservation.error_message = result.error_message;
                            });

                        }else{
                            self.reservation.isAvailable = false;
                        }
                }


                self.reserve = function(){
                    if (self.reservation.isAvailable){
//                        Richiede la prenotazione
                    }
                }



                self.requestBooking = function(){
                    if (!self.reservation.isAvailable){
                        console.log('Reservation unavailable');
                        return;
                    }

                    var options = getQuoteReservationData();



                    if (options.start && options.end && options.numero_ospiti){
                            console.log('options:',options)
                            var url = djangoUrl.reverse('api_alloggio_book',{api_name:'v1',resource_name:'alloggio',pk:self.alloggioId})


                            $http({
                                method: 'GET',
                                url: url,
                                params: options
                            }).success(function (result) {
//                                    self.reservation.isAvailable = true;
////                                    self.reservation.total = result.total;
////                                    self.reservation.caparra = result.caparra;
//                                    self.reservation.quote = result
                                   console.log(result)
                                    if (result.redirect_url){
                                         $window.location.href = result.redirect_url
                                    }
                            }).error(function(result){
//                                    console.log('error:',result)
                                    if (result.error_message){

                                        alert(result.error_message)
                                    }else {
                                        alert('Error')
                                    }
//                                    self.reservation.isAvailable = false;
//                                    self.reservation.error_message = result.error_message;
                            });

                        }

//                    self.reservation.total = Math.random();
//                    console.log('new total: ',self.reservation.total);
//                    console.log(self.filters)
//                    console.log(self.alloggioId)
                }







            }]);

})();