/**
 * Created with PyCharm.
 * User: elfo
 * Date: 10/12/14
 * Time: 15:23
 * To change this template use File | Settings | File Templates.
 */


(function (ng) {
    'use strict';
    var app = ng.module('angular-alloggio-search', [])

    app.directive(
        'ngAlloggioSearch',
        [
            "$parse", '$http', '$timeout', 'ApiAlloggio', '$location', '$filter', '$window',
            function ($parse, $http, $timeout, ApiAlloggio, $location, $filter, $window) {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/alloggio-search/angular-alloggio-search.html',
//                    replace: true,
                    link: {
                        pre: function ($scope, element, attribiutes) {

//                            $scope.$watch(function() {
//                                return $location.path();
//                             }, function(newVal,oldVal  ){
//                               console.log('change location path!!!',oldVal,newVal)
//                                if(oldVal != newVal)
////                                $location.update($location.path())
//                                    $window.location.href = newVal;
//                             });


                            $scope.$watch(function () {
                                return $location.search()
                            }, function (params) {
                                console.log('Update location search', params);
                                $scope.parseFilterFromLocation()
//                                $scope.updateSearch();
//                                if (moment($location.search().checkout).toDate() != $scope.filters.checkout.date)
//                                    $scope.filters.checkout.date = moment($location.search().checkout).toDate();
                            });


                            $scope.parseFilterFromLocation = function () {
                                $scope.filters = {
                                    checkin: {
                                        date: ($location.search().checkin) ?
                                            moment($location.search().checkin).toDate()
                                            : null
                                    },
                                    checkout: {
                                        date: ($location.search().checkout) ?
                                            moment($location.search().checkout).toDate()
                                            : null
                                    },
                                    numero_ospiti: ($location.search().numero_ospiti) ? parseInt($location.search().numero_ospiti) : null
                                }
                            }

                            $scope.parseFilterFromLocation()


                        },
                        post: function ($scope, element, attribiutes) {
//                            $scope.init = true;
                            $scope.datepicker = {}
                            $scope.datepicker.format = "dd MMMM yyyy"
                            $scope.datepicker.options = {
                                formatYear: 'yy',
                                startingDay: 1
                            }


                            $scope.$leftCol = element.find('#leftCol')
                            $scope.$mapCol = element.find('#mapCol')
                            $scope.$searchMap = element.find('#searchMap')
                            $scope.searchResult = []


                            $scope.onResize = function () {
                                $scope.$leftCol.css('height', $scope.$searchMap.innerHeight() + 'px');
                                $scope.$mapCol.css('height', $scope.$searchMap.innerHeight() + 'px');
                            }
                            $scope.onResize();

                            angular.element($window).bind('resize', function () {
                                $scope.onResize();
                            })


//                            try to get map configuration from $location


                            $scope.configMapFromLocation = function () {
                                var defaultConfigMap = {
                                    center: {
                                        latitude: 45.465615676622484,
                                        longitude: 9.191059512615215
                                    },
                                    zoom: 12,
                                    bounds: {}
                                };


                                var mapJson = $location.search().map
                                console.log(mapJson)
                                if (mapJson) {
                                    try {
                                        var map = angular.fromJson(mapJson);
                                    }
                                    catch (err) {
                                        $scope.map = defaultConfigMap;
                                        $location.search('map', null);
                                    }

                                    if (map && map.center && map.center.latitude && map.center.longitude) {

                                        var configMap = angular.extend(defaultConfigMap, map);
//                                        configMap.center = angular.extend(defaultConfigMap.center, map.center);
//                                        configMap.bounds = angular.extend(defaultConfigMap.bounds, map.bounds);
//                                        configMap.bounds.northeast = angular.extend(defaultConfigMap.bounds.northeast, map.bounds.northeast);
//                                        configMap.bounds.southwest = angular.extend(defaultConfigMap.bounds.southwest, map.bounds.southwest);
//                                        console.log(configMap)
                                        $scope.map = configMap;
                                        return;
                                    }
                                }
                                $scope.map = defaultConfigMap;

                            }


                            $scope.configMapFromLocation()

                            $scope.windowOptions = {
                                maxWidth: 200,
                                disableAutoPan: true
                            };


//                            $scope.marker = {
//                                id: 0,
//                                coords: {
//                                    latitude:  45.465615676622484,
//                                    longitude: 9.191059512615215
//                                },
//                                options: {
//                                    draggable: true,
//                                    labelAnchor: "100 0",
//                                    labelClass: "marker-labels"
//                                },
//                                events: {
//                                    dragend: function (marker, eventName, args) {
//                                        console.log('marker dragend');
//                                        var lat = marker.getPosition().lat();
//                                        var lon = marker.getPosition().lng();
//                                          console.log(lat);
//                                          console.log(lon);
//
//                                        $scope.marker.options = {
//                                            draggable: true,
////                                labelContent: "lat: " + $scope.marker.coords.latitude + ' ' + 'lon: ' + $scope.marker.coords.longitude,
//                                            labelContent: $scope.address.formatted_address,
//                                            labelAnchor: "100 0",
//                                            labelClass: "marker-labels"
//                                        };
//
//
//
//                                    }
//                                }
//                            };

//moment('2014-12-17 00:00').toDate()

//                            $scope.$watch('filters',function(){
//                                console.log('update filters')
////                                if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date){
////                                    $location.search('checkin', $filter('date')($scope.filters.checkin.date, "yyyy-MM-dd HH:mm") );
//////                                    if (!$scope.init) $scope.updateSearch();
////                                }
//                            })
                            $scope.$watchCollection('searchResult', function (newValue, oldValue) {
                                if (newValue === oldValue  || angular.equals(newValue, oldValue)) {
                                    return;
                                }
                                $scope.updateSearchMarkers()
                            })


                            $scope.$watch('filters.checkin.date', function (newValue, oldValue) {
                                if (newValue === oldValue) {
                                    return;
                                }

                                if (moment($scope.filters.checkin.date).add(7, 'days').toDate() > $scope.filters.checkout.date) {
                                    $scope.filters.checkout.date = moment($scope.filters.checkin.date).add(7, 'days').toDate();
                                    return;
                                }

                                console.log('update filters.checkin.date', newValue, oldValue)
                                if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date) {
                                    $location.search('checkin', $filter('date')($scope.filters.checkin.date, "yyyy-MM-dd HH:mm"));

                                    if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date)
                                        $scope.updateSearch();
                                }
                            })
                            $scope.$watch('filters.checkout.date', function (newValue, oldValue) {
                                if (newValue === oldValue) {
                                    return;
                                }

                                if (moment($scope.filters.checkout.date).subtract(7, 'days').toDate() < $scope.filters.checkin.date) {
                                    $scope.filters.checkin.date = moment($scope.filters.checkout.date).subtract(7, 'days').toDate();
                                    return;
                                }

                                console.log('update filters.checkout.date', newValue, oldValue)
                                if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date) {
                                    $location.search('checkout', $filter('date')($scope.filters.checkout.date, "yyyy-MM-dd HH:mm"));
                                    if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date)
                                        $scope.updateSearch();
                                }
                            })
                            $scope.$watch('filters.numero_ospiti', function (newValue, oldValue) {
                                if (newValue === oldValue) {
                                    return;
                                }
                                console.log('update filters.numero_ospiti', newValue, oldValue)
                                if ($scope.filters && $scope.filters.numero_ospiti) {
                                    $location.search('numero_ospiti', $scope.filters.numero_ospiti);
                                    $scope.updateSearch();
                                }
                            })

                            $scope.$watch('map.bounds.northeast', function (newValue, oldValue) {
                                if (newValue === oldValue || angular.equals(newValue, oldValue) || typeof oldValue == 'undefined') {
                                    return;
                                }
                                $scope.changeMapBound()
                            })
                            $scope.$watch('map.bounds.southwest', function (newValue, oldValue) {
                                if (newValue === oldValue || angular.equals(newValue, oldValue) || typeof oldValue == 'undefined') {
                                    return;
                                }
                                $scope.changeMapBound()
                            })


                            $scope.changeMapBound = function () {
                                if ($scope.mapDelayPromise) {
                                    $timeout.cancel($scope.mapDelayPromise)
                                }

                                $scope.mapDelayPromise = $timeout(function () {
                                    $location.search('map', angular.toJson($scope.map));
                                    $scope.updateSearch()
                                }, 50)

                            }


                            $scope.updateSearch = function () {
                                var options = {
                                    active: true,
				    limit: 200
                                }

                                if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date)
//                                    options.end = moment($scope.filters.checkout.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) .format('YYYY-MM-DD HH:mm:ss ZZ')
                                    options.end = moment($scope.filters.checkout.date).format('YYYY-MM-DD HH:mm:ss')

                                if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date)
//                                    options.start = moment($scope.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
                                    options.start = moment($scope.filters.checkin.date).format('YYYY-MM-DD HH:mm:ss')

                                if ($scope.filters && $scope.filters.numero_ospiti)
//                                    options.start = moment($scope.filters.checkin.date).format() //"2014-09-08T08:02:17-05:00" (ISO 8601) ('YYYY-MM-DD HH:mm:ss ZZ')
                                    options.numero_ospiti = $scope.filters.numero_ospiti


                                if ($scope.map && $scope.map.bounds &&
                                    $scope.map.bounds.northeast && $scope.map.bounds.northeast.latitude && $scope.map.bounds.northeast.longitude &&
                                    $scope.map.bounds.southwest && $scope.map.bounds.southwest.latitude && $scope.map.bounds.southwest.longitude
                                    ) {

                                    options.bounds_ne_lat = $scope.map.bounds.northeast.latitude;
                                    options.bounds_ne_lng = $scope.map.bounds.northeast.longitude;
                                    options.bounds_sw_lat = $scope.map.bounds.southwest.latitude;
                                    options.bounds_sw_lng = $scope.map.bounds.southwest.longitude;

                                }

                                var tmpResult = ApiAlloggio.query(options, function () {
                                    var remove_id_list = [];
                                    angular.forEach($scope.searchResult, function (value, key) {
                                        var obj = _.find(tmpResult, function (obj) {
                                            return obj.id == value.id
                                        })
                                        if (!obj) {
                                            remove_id_list.push(key)
                                        }
                                    });
                                    angular.forEach(remove_id_list.sort().reverse(), function (idx) {
                                        $scope.searchResult.splice(idx, 1)
                                    })
                                    angular.forEach(tmpResult, function (value, key) {
                                        var obj = _.find($scope.searchResult, function (obj) {
                                            return obj.id == value.id
                                        })
                                        if (!obj) {
                                            $scope.searchResult.push(value);
                                        }
                                    });
                                })

                            }

                            $scope.searchMarkers = [



                            ];

//                            $scope.searchResult = ApiAlloggio.query(null,function(){
//                                $scope.updateSearchMarkers()
//                            })

                            $scope.searchMarkerEvents = {

                                mouseover: function (event, eventName, model, args) {
                                    console.log('searchMarkerEvents mouseover', event, eventName, model, args)
                                }

                            }

                            $scope.searchMarkerLabel = function () {
                                console.log('searchMarkerLabel')
                                return 'cazzibuffi'
                            }

                            $scope.onMarkerClicked = function (marker) {
                                marker.showWindow = true;
                                $scope.$apply();

                                //window.alert("Marker: lat: " + marker.latitude + ", lon: " + marker.longitude + " clicked!!")
                            };
                            $scope.updateSearchMarkers = function () {


//                                 var remove_id_list = [];
//                                    angular.forEach($scope.searchResult, function (value, key) {
//                                        var obj = _.find(tmpResult, function (obj) {
//                                            return obj.id == value.id
//                                        })
//                                        if (!obj) {
//                                            remove_id_list.push(key)
//                                        }
//                                    });
//                                    angular.forEach(remove_id_list.sort().reverse(), function (idx) {
//                                        $scope.searchResult.splice(idx, 1)
//                                    })
//
//                                    console.log('remove_id_list', remove_id_list)
//
////                                    $scope.searchResult = tmpResult;
//
//                                    angular.forEach(tmpResult, function (value, key) {
//                                        var obj = _.find($scope.searchResult, function (obj) {
//                                            return obj.id == value.id
//                                        })
//                                        if (!obj) {
//                                            $scope.searchResult.push(value);
//                                        }
//                                    });

                                $scope.searchMarkers = []

//                                var remove_id_list = [];
//                                angular.forEach($scope.searchMarkers, function (value, key) {
//                                    var obj = _.find($scope.searchResult, function (obj) {
//                                        return obj.id == value.id
//                                    })
//                                    if (!obj) {
//                                        remove_id_list.push(key)
//                                    }
//                                });
//                                angular.forEach(remove_id_list.sort().reverse(), function (idx) {
//                                    $scope.searchMarkers.splice(idx, 1)
//                                })

                                angular.forEach($scope.searchResult, function (value, key) {
//                                        var idx = $scope.valid_optional_services.indexOf(value)
//                                        $scope.valid_optional_services.splice(idx,1);
//                                    console.log('updateSearchMarkers: ', value)
//                                    var obj = _.find($scope.searchMarkers, function (obj) {
//                                        return obj.id == value.id
//                                    })
//                                    console.log('obj for value.id',value.id,obj)
//                                    if (typeof obj == 'undefined'){

                                    var marker = {
                                        alloggio: value,
                                        latitude: value.address.latitude,
                                        longitude: value.address.longitude,
                                        id: value.id,
                                        title: 'Zio cane',
                                        options: {
                                            draggable: false,
                                            labelAnchor: "100 0",
                                            labelClass: "marker-labels",
                                            labelContent: 'Peppo lasagna'
                                        }
                                    }

                                    this.push(marker)
//                                    }


                                }, $scope.searchMarkers);

                                console.log('$scope.searchMarkers: ', $scope.searchMarkers)
//                                $timeout(function () {
//                                $scope.$apply(function () {
//                                    $scope.message = "Timeout called!";
//                                });
//                            }, 500);
                            }


                            $scope.openDatepicker = function ($event, ref) {
                                console.log('openDatepicker', $event, ref)
                                $event.preventDefault();
                                $event.stopPropagation();
                                if (ref == 'in') {
                                    console.log('open IN')
                                    $scope.filters.checkin.open = true;

                                } else if (ref == 'out') {
                                    console.log('open OUT')
                                    $scope.filters.checkout.open = true;

                                }
                            }


                            $scope.click = function (alloggio) {
                                console.log('click alloggio', alloggio)
                            }

                            $scope.updateSearch();

                        }
                    }
                };
            }
        ]
    );

})(window.angular);
