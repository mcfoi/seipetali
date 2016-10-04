/**
 * Created with PyCharm.
 * User: elfo
 * Date: 10/12/14
 * Time: 15:23
 * To change this template use File | Settings | File Templates.
 */


(function (ng) {
    'use strict';
    var app = ng.module('angular-optional-services', [])

        app.directive(
        'ngOptionalServices',
        [
            "$parse", '$http', '$timeout', 'FileUploader','djangoUrl','ApiIva','ApiServizioOpzionale',
            function ($parse, $http, $timeout, FileUploader,djangoUrl,ApiIva,ApiServizioOpzionale) {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/optional-services/angular-optional-services.html',
//                    replace: true,
                    link: {
                        pre: function ($scope, element, attribiutes) {

                             $scope.dragControlServicesListeners = {
                                accept: function (sourceItemHandleScope, destSortableScope) {
    //                                console.log('Accept?',sourceItemHandleScope, destSortableScope)
                                    return true
                                },//override to determine drag is allowed or not. default is true.
                                itemMoved: function (event) {
                                    console.log('itemMoved')
                                //Do what you want},
                                },
                                orderChanged: function(event) {
                                    console.log('orderChanged')
//                                    $scope.gallerySavePhotos()
                                //Do what you want
                                },
                                dragStart: function(event) {
                                    console.log('dragStart')
                                //Do what you want
                                },
                                dragEnd: function(event) {
                                    console.log('dragEnd')
                                //Do what you want
                                },
                                containment: '#service-sortable-container',
//                                additionalPlaceholderClass: 'pull-left'
    //                            containment: '#board'//optional param.
                            };
                        },
                        post:function ($scope, element, attribiutes) {

                            console.log('attributes',attribiutes)
                            $scope.initActiveService = false;
                            if (attribiutes.activeServices){
//                                console.log('!!!',angular.fromJson(attribiutes.activeServices));
                                $scope.initActiveService = angular.fromJson(attribiutes.activeServices);
                            }

//                            $scope.avilableServices = [];
                            $scope.active_services = [];

                            $scope.service_form = {};
                            $scope.valid_iva = [];
                            $scope.valid_iva = ApiIva.query()

//                            $scope.valid_optional_services = [];
//
//
//                            $scope.$watch('valid_optional_services', function (newVal, oldVal) {
//                                console.log('WATCH valid_optional_services:', newVal,oldVal);
//                            });

                            $scope.availableServices = function () {
                                return $scope.valid_optional_services.filter(function (service) {
                                  return $scope.active_services.indexOf(service) == -1;
                                });
                              };

                            $scope.valid_optional_services = ApiServizioOpzionale.query(null,function(){

//                                Prima inizializzazione dei servizi opzionali disponibili.
//                                Creo $scope.active_services che contiene i servizo definiti come attributo della direttiva filtrando il risultato della query/
//                                poi li rimuovo dalla lista iniziale $scope.valid_optional_services per non avere doppioni.
                                if ( $scope.initActiveService){

                                    $scope.active_services = $scope.valid_optional_services.filter(function (service) {
                                          return $scope.initActiveService.indexOf(service.id) !== -1;
                                    });

                                    angular.forEach($scope.active_services, function(value, key) {
                                        var idx = $scope.valid_optional_services.indexOf(value)
                                        $scope.valid_optional_services.splice(idx,1);
                                    });

                                }
                            });



//                            $scope.active_services_id = function(){
//                                var idList = [];
//                                angular.forEach($scope.active_services, function(value, key) {
//                                      this.push(value.id);
//                                    }, idList);
//                                return idList;
//                            }

                            $scope.formVisible = false;

                            $scope.cancelForm = function(event){
                                event.preventDefault();
                                console.log('cancelForm')
                                $scope.service_form = {};
                                $scope.formVisible = false;
                            }




                            $scope.time_factor_values = [
                                {name:'alla settimana', value:7},
                                {name:'al giorno', value:1},
                            ]
                            $scope.service_form.fattore_tempo = 1;


                            $scope.addOptionalServices = function(event){
                                console.log('addOptionalServices',event)
                                event.preventDefault();

                                var servizio = ApiServizioOpzionale._create_resource($scope.service_form)

//                                servizio.success(function(response, status, headers) {
//                                    $scope.valid_optional_services = ApiServizioOpzionale.query();
//
////                                    return _this._config.detail_url = headers("Location");
//                                });
                                servizio.post().success(function(response, status, headers) {
//                                    return _this._config.detail_url = headers("Location");
//                                    console.log(response)
                                    $scope.active_services.push(response)
//                                    $scope.valid_optional_services = ApiServizioOpzionale.query();
                                     $scope.service_form = {};
                                     $scope.formVisible = false;

                                  });

//                                servizio.post().then(function(){
//
////                                    In caso di successo
//                                }, function(reason) {
////                                    In caso di fallimento
//                                    console.log(reason)
//
//                                })



                            }


                        }
                    }
                };
            }
        ]
    );

})(window.angular);
//
//.then(function(){
//
//                                    $scope.active_services.push(servizio)
////                                    $scope.valid_optional_services = ApiServizioOpzionale.query();
//                                     $scope.service_form = {};
//                                     $scope.formVisible = false;
//                                }, function(reason) {
////                                    In caso di fallimento
//                                    console.log(reason)
//                                  // error: handle the error if possible and
//                                  //        resolve promiseB with newPromiseOrValue,
//                                  //        otherwise forward the rejection to promiseB
////                                  if (canHandle(reason)) {
////                                   // handle the error and recover
////                                   return newPromiseOrValue;
////                                  }
////                                  return $q.reject(reason);
//                                })