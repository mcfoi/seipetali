/**
 * Created with PyCharm.
 * User: elfo
 * Date: 15/12/14
 * Time: 16:22
 * To change this template use File | Settings | File Templates.
 */





(function (ng) {
    'use strict';
    var app = ng.module('angular-alloggio-calendar', [])

    app.directive(
        'ngAlloggioCalendar',
        [
            "$parse","ApiEvent",'ApiCalendar','uiCalendarConfig','$http','$compile',
            function ($parse,ApiEvent,ApiCalendar,uiCalendarConfig,$http,$compile) {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/alloggio-calendar/angular-alloggio-calendar.html',
//                    replace: true,
                    link: {
                        pre: function ($scope, element, attribiutes) {



                            $scope.onDayClick = function(date, jsEvent, view ){
                                console.log('ngAlloggioCalendar onDayClick',date, jsEvent, view)
                            }
                            $scope.OnEventDrop = function(){
                                console.log('ngAlloggioCalendar OnEventDrop')
                            }
                            $scope.OnEventResize = function(){
                                console.log('ngAlloggioCalendar OnEventResize')
                            }
                            $scope.selectEvent = function(start, end, jsEvent, view ){
                                console.log('ngAlloggioCalendar selectEvent' )
                                    console.log(typeof start,start)
                                console.log(typeof end,end)

                                 var event = ApiEvent._create_resource({
                                        start:start,
                                        end:end,
                                        title:'blocked',
                                        description:'blocked',
                                        calendar: $scope.mycalendar.resource_uri
                                 })

                                    event.post().success(function(response, status, headers) {
                                    console.log(response)
                                    $scope.events.push(response)

                                  });


                            }

                            $scope.onViewRender = function(view, element) {
                               console.log("View Changed: ", view.visStart, view.visEnd, view.start, view.end);

                                $scope.events.splice(0);
                                var tmpevents = ApiEvent.query({
                                    calendar__alloggio__id:attribiutes.alloggioId,
                                    start__gte:view.start.toISOString(),
                                    end__lte:view.end.toISOString()
                                },function(){
                                    angular.forEach(tmpevents,function(value){
//                                        console.log('Nuovi eventi:',value)
                                        $scope.events.push(value)
                                    })
                                })

                            }

                            $scope.remove = function(index) {
                              console.log($scope.events[index]);

                                return $http.delete($scope.events[index].resource_uri).success(function(){
                                    console.log("delete successful");
                                    $scope.events.splice(index,1);
                                });

                            };

                            $scope.onEventMouseover = function( event, jsEvent, view ) {
                                    var idx = -1;
                                    angular.forEach($scope.events, function(value, key) {
                                        if (value.id == event.id){
                                            idx = key;
                                        }
                                    });
                                    $scope.events[idx].hover = true;

                            }
                            $scope.onEventMouseout = function( event, jsEvent, view ) {
//                                  event.hover = false;
                                    var idx = -1;
                                    angular.forEach($scope.events, function(value, key) {
                                        if (value.id == event.id){
                                            idx = key;
                                        }
                                    });

                                    $scope.events[idx].hover = false;


                            }

                            $scope.onEventRender = function( event, element, view ) {
//                                console.log(event)
//                                event.color='#00f'
//                                event.textColor='#0ff'
//                                if(event.reservation.length) {
//                                    element.css('background-color', '#0ff');
//                                }
                                element.attr({'tooltip': event.title,
                                             'tooltip-append-to-body': true});

                                $compile(element)($scope);
                            };

//                            $scope.eventSources = [];
                            var date = new Date();
                            var d = date.getDate();
                            var m = date.getMonth();
                            var y = date.getFullYear();
//
//                            $scope.calEventsExt = {
//           color: '#f00',
//           textColor: 'yellow',
//           events: [
//              {type:'party',title: 'Lunch',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//              {type:'party',title: 'Lunch 2',start: new Date(y, m, d, 12, 0),end: new Date(y, m, d, 14, 0),allDay: false},
//              {type:'party',title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
//            ]
//        };
//                            $scope.events = [
////          {title: 'All Day Event',start: new Date(y, m, 1),url: 'http://www.angularjs.org'},
//          {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
//          {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: false},
//          {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: true}];
//                            $scope.events = [
//                              {title: 'All Day Event',start: new Date(y, m, 1)},
//                              {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
//                              {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: false},
//                              {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: false},
//                              {title: 'Birthday Party',start: new Date(y, m, d + 1, 19, 0),end: new Date(y, m, d + 1, 22, 30),allDay: false},
//                              {title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
//                            ];

                            $scope.events = [];

                            if (attribiutes.alloggioId){
                                console.log('!!!',attribiutes.alloggioId);
//                                $scope.initActiveService = angular.fromJson(attribiutes.activeServices);
//                                $scope.events = ApiEvent.query({
//                                    calendar__alloggio__id:attribiutes.alloggioId
//                                })

                                $scope.calendars = ApiCalendar.query({alloggio__id:attribiutes.alloggioId},function(){
                                    $scope.mycalendar = $scope.calendars[0];
                                });
                            }


//                            $scope.configEvents = {
//                                    color:'#f00',
//                                    textColor: '#0f0',
//                                    events:$scope.events
//                                }

                            $scope.eventSources = [
//                                $scope.events
                                {
//                                    color:'#f00',
//                                    textColor: '#0f0',
                                    events:$scope.events
                                }
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
                              calendar:{
                                height: 450,
                                editable: true,
                                selectable: true,
                                selectOverlap: false,
                                timezone: 'local',
//                                  timezone:false,
                                  currentTimezone: "local",
                                  ignoreTimezone: false,
                                header:{
//                                  left: 'month basicWeek basicDay agendaWeek agendaDay',
                                    left:'',
                                  center: 'title',
                                  right: 'today prev,next'
                                },
                                dayClick: $scope.onDayClick,
                                eventDrop: $scope.OnEventDrop,
                                eventResize: $scope.OnEventResize,
                                select: $scope.selectEvent,
                                viewRender: $scope.onViewRender,
                                eventMouseover:$scope.onEventMouseover,
                                eventMouseout:$scope.onEventMouseout,
                                eventRender: $scope.onEventRender
                              }
                            };


                        },
                        post: function ($scope, element, attribiutes) {

//                            console.log('DIOCANE',uiCalendarConfig)


                        }
                    }
                };
            }
        ]
    );

})(window.angular);
