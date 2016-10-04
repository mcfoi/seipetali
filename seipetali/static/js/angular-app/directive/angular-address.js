/**
 * Created with PyCharm.
 * User: elfo
 * Date: 05/12/14
 * Time: 14:51
 * To change this template use File | Settings | File Templates.
 */

(function (ng,google) {
    'use strict';
        var app = ng.module('angular-address', [])
    console.log('init angular-address');
    console.log(google);
    var geocoder = new google.maps.Geocoder()


    app.directive(
        'ngaddress',
        [
            "$parse",'$http','$timeout',
            function ($parse,$http,$timeout)
            {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/address/angular-address.html',
                    replace: true,
                    link: function($scope, element, attribiutes) {

//                        disabilito il form submittin da userInputAddress e verifico l'inidirizzo
                        $(element).find('#userInputAddress').bind("keydown keypress", function(event) {
                            if(event.which === 13) {
                               $scope.checkAddress(event);
                            }
                        });

//                        console.log('attribiutes',attribiutes);

//                        Form structure
                        $scope.form = {};
                        $scope.form.country =  {name: null, code: null};
                        $scope.form.state =  {name: null, code: null,country:null};
                        $scope.form.locality =  {name: null, postal_code: null};
                        $scope.form.address =  {street_address: null, street_number: null,formatted: null,latitude: null,longitude: null};


                        $scope.address = {};

                        $scope.map = { center: { latitude: 0, longitude: 0 }, zoom: 8 };
                        $scope.coordsUpdates = 0;
                        $scope.dynamicMoveCtr = 0;
                        $scope.options = {scrollwheel: false};

                        $scope.mapVisible = false;



                        $scope.marker = {
                          id: 0,
                          coords: {
                            latitude: (attribiutes.addressLatitude && attribiutes.addressLatitude != 'None') ? attribiutes.addressLatitude :40.1451,
                            longitude: (attribiutes.addressLongitude && attribiutes.addressLongitude != 'None') ? attribiutes.addressLongitude: -99.6680
                          },
                          options: {
                                draggable: true ,
                                labelAnchor: "100 0",
                                labelClass: "marker-labels"
                          },
                          events: {
                            dragend: function (marker, eventName, args) {
                              console.log('marker dragend');
                              var lat = marker.getPosition().lat();
                              var lon = marker.getPosition().lng();
//                              console.log(lat);
//                              console.log(lon);

                              $scope.marker.options = {
                                draggable: true,
//                                labelContent: "lat: " + $scope.marker.coords.latitude + ' ' + 'lon: ' + $scope.marker.coords.longitude,
                                  labelContent:$scope.address.formatted_address,
                                labelAnchor: "100 0",
                                labelClass: "marker-labels"
                              };

                                var latlng = new google.maps.LatLng(lat, lon);

                                geocoder.geocode({'latLng':latlng},function(result,status){
                                console.log(result,status)


                                if (status == 'OK'){

                                    $scope.$apply(function () {
                                        $scope.mapVisible = true;
                                        $scope.first_result = result[0];
                                        $scope.address.formatted_address = $scope.first_result.formatted_address;
                                        $scope.address.address = $scope.first_result.formatted_address;
                                        $scope.map.center.latitude = $scope.first_result.geometry.location.lat();
                                        $scope.map.center.longitude = $scope.first_result.geometry.location.lng();
                                        $scope.map.zoom = 19;

                                        $scope.marker.coords.latitude = $scope.first_result.geometry.location.lat();
                                        $scope.marker.coords.longitude = $scope.first_result.geometry.location.lng();
                                        $scope.marker.options.labelContent = $scope.address.formatted_address;

                                         $scope.setAddress($scope.first_result);
                                    });
                                }
                            })



                            }
                          }
                        };



                         if (attribiutes.addressFormatted && attribiutes.addressFormatted != 'None'){
                            console.log('addressFormatted')
                             $scope.address.address = attribiutes.addressFormatted;
                            geocoder.geocode({'address':attribiutes.addressFormatted},function(result,status){
                                console.log(result,status)


                                if (status == 'OK'){

                                    $scope.$apply(function () {
                                        $scope.mapVisible = true;
                                        $scope.first_result = result[0];
//                                        $scope.address.formatted_address = $scope.first_result.formatted_address;
                                        $scope.map.center.latitude = $scope.first_result.geometry.location.lat();
                                        $scope.map.center.longitude = $scope.first_result.geometry.location.lng();
                                        $scope.map.zoom = 19;

//                                        $scope.marker.coords.latitude = $scope.first_result.geometry.location.k;
//                                        $scope.marker.coords.longitude = $scope.first_result.geometry.location.B;
                                        $scope.marker.options.labelContent = $scope.address.formatted_address;


                                        $scope.setAddress($scope.first_result);

                                    });
                                }
                            })
                        }



                         $scope.$watchCollection("marker.coords", function (newVal, oldVal) {
                          if (_.isEqual(newVal, oldVal))
                            return;
                          $scope.coordsUpdates++;
                        });











                        $scope.checkAddress = function(e){
                            e.preventDefault();


                            geocoder.geocode({'address':$scope.address.address},function(result,status){
                                console.log(result,status)


                                if (status == 'OK'){

                                    $scope.$apply(function () {
                                        $scope.mapVisible = true;
                                        $scope.first_result = result[0];
                                        $scope.address.formatted_address = $scope.first_result.formatted_address;
                                        $scope.address.address = $scope.first_result.formatted_address;
                                        $scope.map.center.latitude = $scope.first_result.geometry.location.lat();
                                        $scope.map.center.longitude = $scope.first_result.geometry.location.lng();
                                        $scope.map.zoom = 19;

                                        $scope.marker.coords.latitude = $scope.first_result.geometry.location.lat();
                                        $scope.marker.coords.longitude = $scope.first_result.geometry.location.lng();
                                        $scope.marker.options.labelContent = $scope.address.formatted_address;


                                        $scope.setAddress($scope.first_result);
                                    });
                                }
                            })

//                            $http({
//                                method: 'GET',
//                                url: '/api/v1/address/check',
//                                params: $scope.address,
//                                data: { applicationId: 3 }
//
//                            }).success(function (result) {
//                                    console.log(result)
//                            });


                        }





                        $scope.setAddress = function(address){
                            console.log('set address',address);

                            if (address.types[0] != "street_address"){
                                alert ('Devi specificare un indirizzo completo',address.types[0]);
                                return;
                            }

//                            $scope.form.country =  {name: null, code: null};
//                            $scope.form.state =  {name: null, code: null,country:null};
//                            $scope.form.locality =  {name: null, postal_code: null};
//                            $scope.form.address =  {street_address: null, street_number: null,formatted: null,latitude: null,longitude: null};

                            $scope.form.address =  {formatted: address.formatted_address,latitude: address.geometry.location.lat() ,longitude: address.geometry.location.lng()};

                            angular.forEach(address.address_components, function(value, key) {
//                                console.log(value, key)

                                if (value.types.toString() == ["country","political"].toString()){
                                    $scope.form.country = {name: value.long_name, code: value.short_name};;
                                } else if (value.types.toString() == ["postal_code"].toString()){
                                    $scope.form.locality.postal_code = value.long_name;
                                } else if (value.types.toString() == ["administrative_area_level_2","political"].toString()){
                                    $scope.form.locality.name = value.long_name;
                                } else if (value.types.toString() == ["locality","political"].toString()){
                                    $scope.form.locality.name = value.long_name;
                                } else if (value.types.toString() == ["street_number"].toString()){
                                    $scope.form.address.street_number = value.long_name;
                                } else if (value.types.toString() == ["route"].toString()){
                                    $scope.form.address.street_address = value.long_name;
                                }else if (value.types.toString() == ["administrative_area_level_1","political"].toString()){
                                    $scope.form.state.name = value.long_name;
//                                    $scope.form.state.code = value.short_name;
                                }




                            });





                        }


                        $scope.getLocation = function(val) {
                            return $http.get('http://maps.googleapis.com/maps/api/geocode/json', {
                              params: {
                                address: val,
                                sensor: false
                              }
                            }).then(function(response){
                              return response.data.results.map(function(item){
                                return item.formatted_address;
                              });
                            });
                          };

//                        var params = {
//                            barColors: $parse(attribiutes.barColors)($scope),
//                            stacked: MorrisOptionsParser.parseValues(attribiutes.stacked)
//                        },
//                            graph;
//
//                        extendDeep(
//                            params,
//                            MorrisOptionsParser.getBasicOptions(element, attribiutes, $scope),
//                            MorrisOptionsParser.getValuesOptions(attribiutes, $scope),
//                            MorrisOptionsParser.getGridOptions(attribiutes)
//                        );
//
//                        graph = M.b(MorrisOptionsParser.parse(params));
//                        MorrisOptionsParser.addCallbackForGraph(attribiutes, $scope, graph);
                    }
                };
            }
        ]
    );

//    var app = ng.module('angular-address', []),
//        extendDeep = function (dst) {
//            angular.forEach(arguments, function(obj) {
//                if (obj !== dst) {
//                    angular.forEach(obj, function(value, key) {
//                        if (dst[key] && dst[key].constructor && dst[key].constructor === Object) {
//                            extendDeep(dst[key], value);
//                        } else {
//                            dst[key] = value;
//                        }
//                    });
//                }
//            });
//            return dst;
//        };

//    app.factory(
//       'Morris',
//        [
//            function ()
//            {
//                return {
//                    b: Morris.Bar,
//                    l: Morris.Line,
//                    a: Morris.Area,
//                    d: Morris.Donut
//                };
//            }
//        ]
//    );

//    app.service(
//        'MorrisOptionsParser',
//        [
//            "$parse",
//            function ($parse)
//            {
//                this.parseValues = function (value, possibleValues, skipBoolTransform)
//                {
//                    if (!ng.isDefined(possibleValues)) {
//                        possibleValues = [];
//                    }
//
//                    if (!ng.isDefined(value)) {
//                        return undefined;
//                    }
//
//                    if (possibleValues.indexOf(value) !== -1) {
//                        return value;
//                    }
//
//                    if (skipBoolTransform !== true) {
//                        if (value === "true") {
//                            return true;
//                        } else if (value === "false") {
//                            return false;
//                        }
//                    }
//
//                    return undefined;
//                };
//
//                this.getBasicOptions = function (element, attribiutes, $scope)
//                {
//                    return {
//                        element: element,
//                        data: $parse(attribiutes.data)($scope),
//                        additional: {
//                            resize: this.parseValues(attribiutes.resize)
//                        }
//                    };
//                };
//
//                this.getValuesOptions = function (attribiutes, $scope)
//                {
//                    return {
//                        xkey: attribiutes.xkey,
//                        ykeys: $parse(attribiutes.ykeys)($scope),
//                        labels: $parse(attribiutes.labels)($scope),
//                        hideHover: this.parseValues(attribiutes.hideHover, ['always', 'auto']),
//                        asFunctions: {
//                            hoverCallback: $parse(attribiutes.hoverCallback)($scope)
//                        }
//                    }
//                };
//
//                this.getGridOptions = function (attribiutes)
//                {
//                    return {
//                        axes: this.parseValues(attribiutes.axes),
//                        grid: this.parseValues(attribiutes.grid),
//                        additional: {
//                            gridTextColor: attribiutes.gridTextColor,
//                            gridTextSize: attribiutes.gridTextSize,
//                            gridTextFamily: attribiutes.gridTextFamily,
//                            gridTextWeight: attribiutes.gridTextWeight
//                        }
//                    };
//                };
//
//                this.getLinesOptions = function (attribiutes, $scope)
//                {
//                    return {
//                        lineColors: $parse(attribiutes.lineColors)($scope),
//                        lineWidth: attribiutes.lineWidth,
//                        pointSize: attribiutes.pointSize,
//                        pointFillColors: $parse(attribiutes.pointFillColors)($scope),
//                        pointStrokeColors: attribiutes.pointStrokeColors,
//                        ymax: attribiutes.ymax,
//                        ymin: attribiutes.ymin,
//                        smooth: this.parseValues(attribiutes.smooth),
//                        parseTime: this.parseValues(attribiutes.parseTime),
//                        postUnits: attribiutes.postUnits,
//                        preUnits: attribiutes.preUnits,
//                        xLabels: attribiutes.xLabels,
//                        xLabelAngle: attribiutes.xLabelAngle,
//
//                        goals: $parse(attribiutes.goals)($scope),
//                        events: $parse(attribiutes.events)($scope),
//
//                        additional: {
//                            fillOpacity: attribiutes.fillOpacity,
//
//                            goalStrokeWidth: attribiutes.goalStrokeWidth,
//                            goalLineColors: attribiutes.goalLineColors,
//
//                            eventStrokeWidth: attribiutes.eventStrokeWidth,
//                            eventLineColors: attribiutes.eventLineColors,
//
//                            continuousLine: this.parseValues(attribiutes.continuousLine)
//                        },
//                        asFunctions: {
//                            dateFormat: $parse(attribiutes.dateFormat)($scope),
//                            xLabelFormat: $parse(attribiutes.xLabelFormat)($scope)
//                        }
//                    };
//                };
//
//                this.parse = function (params)
//                {
//                    ng.forEach(params.asFunctions, function (value, key) {
//                        if (ng.isFunction(value)) {
//                            params[key] = value;
//                        }
//                    });
//
//                    ng.forEach(params.additional, function (value, key) {
//                        if (ng.isDefined(value)) {
//                            params[key] = value;
//                        }
//                    });
//
//                    return params;
//                };
//
//                this.addCallbackForGraph = function (attribiutes, $scope, graph)
//                {
//                    if (ng.isDefined(attribiutes.setGraph)) {
//                        var setGraphCallback = $parse(attribiutes.setGraph)($scope);
//
//                        if (ng.isFunction(setGraphCallback)) {
//                            setGraphCallback(graph);
//                        }
//                    }
//                };
//            }
//        ]
//    );

//    app.directive(
//        'barChart',
//        [
//            "$parse", "Morris", "MorrisOptionsParser",
//            function ($parse, M, MorrisOptionsParser)
//            {
//                return {
//                    restrict: 'AE',
//                    template: '<div></div>',
//                    replace: true,
//                    link: function($scope, element, attribiutes) {
//                        var params = {
//                            barColors: $parse(attribiutes.barColors)($scope),
//                            stacked: MorrisOptionsParser.parseValues(attribiutes.stacked)
//                        },
//                            graph;
//
//                        extendDeep(
//                            params,
//                            MorrisOptionsParser.getBasicOptions(element, attribiutes, $scope),
//                            MorrisOptionsParser.getValuesOptions(attribiutes, $scope),
//                            MorrisOptionsParser.getGridOptions(attribiutes)
//                        );
//
//                        graph = M.b(MorrisOptionsParser.parse(params));
//                        MorrisOptionsParser.addCallbackForGraph(attribiutes, $scope, graph);
//                    }
//                };
//            }
//        ]
//    );

//    app.directive(
//        'lineChart',
//        [
//            "Morris", "MorrisOptionsParser",
//            function (M, MorrisOptionsParser)
//            {
//                return {
//                    restrict: 'AE',
//                    template: '<div></div>',
//                    replace: true,
//                    link: function($scope, element, attribiutes) {
//                        var params = {},
//                            graph;
//
//                        extendDeep(
//                            params,
//                            MorrisOptionsParser.getBasicOptions(element, attribiutes, $scope),
//                            MorrisOptionsParser.getValuesOptions(attribiutes, $scope),
//                            MorrisOptionsParser.getGridOptions(attribiutes),
//                            MorrisOptionsParser.getLinesOptions(attribiutes, $scope)
//                        );
//
//                        graph = M.l(MorrisOptionsParser.parse(params));
//                        MorrisOptionsParser.addCallbackForGraph(attribiutes, $scope, graph);
//                    }
//
//                };
//            }
//        ]
//    );

//    app.directive(
//        'areaChart',
//        [
//            "Morris", "MorrisOptionsParser",
//            function (M, MorrisOptionsParser)
//            {
//                return {
//                    restrict: 'AE',
//                    template: '<div></div>',
//                    replace: true,
//                    link: function($scope, element, attribiutes) {
//                        var params = {
//                            behaveLikeLine: MorrisOptionsParser.parseValues(attribiutes.behaveLikeLine)
//                        },
//                            graph;
//
//                        extendDeep(
//                            params,
//                            MorrisOptionsParser.getBasicOptions(element, attribiutes, $scope),
//                            MorrisOptionsParser.getValuesOptions(attribiutes, $scope),
//                            MorrisOptionsParser.getGridOptions(attribiutes),
//                            MorrisOptionsParser.getLinesOptions(attribiutes, $scope)
//                        );
//
//                        graph = M.a(MorrisOptionsParser.parse(params));
//                        MorrisOptionsParser.addCallbackForGraph(attribiutes, $scope, graph);
//                    }
//
//                };
//            }
//        ]
//    );

//    app.directive(
//        'donutChart',
//        [
//            "$parse", "Morris", "MorrisOptionsParser",
//            function ($parse, M, MorrisOptionsParser)
//            {
//                return {
//                    restrict: 'AE',
//                    template: '<div></div>',
//                    replace: true,
//                    link: function($scope, element, attribiutes) {
//                        var params = {
//                            colors: $parse(attribiutes.colors)($scope),
//                            asFunctions: {
//                                formatter: $parse(attribiutes.formatter)($scope)
//                            }
//                        },
//                            graph;
//
//                        extendDeep(
//                            params,
//                            MorrisOptionsParser.getBasicOptions(element, attribiutes, $scope)
//                        );
//
//                        graph = M.d(MorrisOptionsParser.parse(params));
//                        MorrisOptionsParser.addCallbackForGraph(attribiutes, $scope, graph);
//                    }
//
//                };
//            }
//        ]
//    );
})(window.angular,window.google);