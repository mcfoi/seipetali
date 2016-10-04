/**
 * Created with PyCharm.
 * User: elfo
 * Date: 16/12/14
 * Time: 14:15
 * To change this template use File | Settings | File Templates.
 */

(function () {
    'use strict';

    angular.module('seipetali-app')
        .controller('alloggioCalendarCtrl', ['$scope', "ApiEvent", 'ApiCalendar', 'uiCalendarConfig', '$http', '$compile',
            function ($scope, ApiEvent, ApiCalendar, uiCalendarConfig, $http, $compile) {


                $scope.onDayClick = function (date, jsEvent, view) {
                    console.log('ngAlloggioCalendar onDayClick', date, jsEvent, view)
                }
                $scope.OnEventDrop = function () {
                    console.log('ngAlloggioCalendar OnEventDrop')
                }
                $scope.OnEventResize = function () {
                    console.log('ngAlloggioCalendar OnEventResize')
                }
                $scope.selectEvent = function (start, end, jsEvent, view) {
                    console.log('ngAlloggioCalendar selectEvent')
                    console.log(typeof start, start)
                    console.log(typeof end, end)

                    var event = ApiEvent._create_resource({
                        start: start,
                        end: end,
                        title: 'foo',
                        description: 'bar',
                        calendar: $scope.mycalendar.resource_uri
                    })

                    event.post().success(function (response, status, headers) {
                        console.log(response)
                        $scope.events.push(response)


                    });


                }

                $scope.onViewRender = function (view, element) {
                    console.log("View Changed: ", view.visStart, view.visEnd, view.start, view.end);
                    console.log('uiCalendarConfig:', uiCalendarConfig)

                    console.log('$scope.calendar', $scope.calendar)
                    console.log('uiCalendarConfig', uiCalendarConfig)
                    console.log('$scope.uiConfig', $scope.uiConfig)
                    console.log('$scope.alloggioCalendar', $scope.alloggioCalendar)
//                                $scope.alloggioCalendar[0].fullCalendar('renderEvent',  $scope.eventSources, true);

                    console.log('$scope.alloggioCalendar[0]', $scope.alloggioCalendar[0])

                    console.log($($scope.alloggioCalendar[0]).fullCalendar('render'))
//                                $($scope.alloggioCalendar[0]).fullCalendar('changeView',view)


//                                 $scope.events = ApiEvent.query({
//                                    calendar__alloggio__id:attribiutes.alloggioId,
//                                    star__gte:view.start.toISOString(),
//                                    end__lte:view.end.toISOString()
//                                })

                    $scope.events.splice(0)
                                                     $scope.events = ApiEvent.query({
                                    calendar__alloggio__id:attribiutes.alloggioId,
                                    star__gte:view.start.toISOString(),
                                    end__lte:view.end.toISOString()
                                })


                }

                $scope.remove = function (index) {
                    console.log($scope.events[index]);

                    return $http.delete($scope.events[index].resource_uri).success(function () {
                        console.log("delete successful");
                        $scope.events.splice(index, 1);
                    });

                };

                $scope.onEventMouseover = function (event, jsEvent, view) {

                    var idx = -1;
                    angular.forEach($scope.events, function (value, key) {
                        if (value.id == event.id) {
                            idx = key;
                        }
                    });

                    $scope.events[idx].hover = true;

                }
                $scope.onEventMouseout = function (event, jsEvent, view) {
//                                  event.hover = false;
                    var idx = -1;
                    angular.forEach($scope.events, function (value, key) {
                        if (value.id == event.id) {
                            idx = key;
                        }
                    });

                    $scope.events[idx].hover = false;


                }

                $scope.onEventRender = function (event, element, view) {
                    element.attr({'tooltip': event.title,
                        'tooltip-append-to-body': true});
                    $compile(element)($scope);
                };


                $scope.events = [];

                var attribiutes = {alloggioId: 4}

                if (attribiutes.alloggioId) {
                    console.log('!!!', attribiutes.alloggioId);
//                                $scope.initActiveService = angular.fromJson(attribiutes.activeServices);
                    var events = ApiEvent.query({
                        calendar__alloggio__id: attribiutes.alloggioId
                    }, function () {

                        angular.forEach(events, function (value, key) {
                                console.log('value::', value)
                                this.push(value)
                            },
                            $scope.events
                        )

                    })


                    $scope.calendars = ApiCalendar.query({alloggio__id: attribiutes.alloggioId}, function () {
                        $scope.mycalendar = $scope.calendars[0];
                    });
                }


//                            $scope.configEvents = {
//                                    color:'#f00',
//                                    textColor: '#0f0',
//                                    events:$scope.events
//                                }
//   var date = new Date();
//    var d = date.getDate();
//    var m = date.getMonth();
//    var y = date.getFullYear();
//
//                            $scope.events = [
//                                      {type:'party',title: 'Lunch',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//                                      {type:'party',title: 'Lunch 2',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//                                      {type:'party',title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
//                                    ]

                $scope.eventSources = [
                    $scope.events
//                                {
//                                    color:'#f00',
//                                    textColor: '#0f0',
//                                    events:$scope.events
//                                }
//                                $scope.calEventsExt
//                                {
//                                   color: '#f00',
//                                   textColor: 'yellow',
//                                   events: [
//                                      {type:'party',title: 'Lunch',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//                                      {type:'party',title: 'Lunch 2',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//                                      {type:'party',title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
//                                    ]
//                                }
                ];

                $scope.uiConfig = {
                    calendar: {
                        height: 450,
                        editable: true,
                        selectable: true,
                        selectOverlap: false,
                        timezone: 'local',
//                                  timezone:false,
                        currentTimezone: "local",
                        ignoreTimezone: false,
                        header: {
//                                  left: 'month basicWeek basicDay agendaWeek agendaDay',
                            left: '',
                            center: 'title',
                            right: 'today prev,next'
                        },
                        dayClick: $scope.onDayClick,
                        eventDrop: $scope.OnEventDrop,
                        eventResize: $scope.OnEventResize,
                        select: $scope.selectEvent,
                        viewRender: $scope.onViewRender,
                        eventMouseover: $scope.onEventMouseover,
                        eventMouseout: $scope.onEventMouseout,
                        eventRender: $scope.onEventRender
                    }
                };


            }]);

})();