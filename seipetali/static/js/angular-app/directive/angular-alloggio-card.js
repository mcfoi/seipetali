/**
 * Created with PyCharm.
 * User: elfo
 * Date: 10/12/14
 * Time: 15:23
 * To change this template use File | Settings | File Templates.
 */


(function (ng) {
    'use strict';
    var app = ng.module('angular-alloggio-card', [])

    app.directive(
        'ngAlloggioCard',
        [
            "$parse","ApiGallery",'djangoUrl','$location','jQuery','$window',
            function ($parse,ApiGallery,djangoUrl,$location,$,$window) {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/alloggio-search/angular-alloggio-card.html',
//                    replace: true,
                    scope: {
                      // same as '=customer'
                      alloggio: '=',
                      filters: '='
                    },
                    link: {
                        pre: function ($scope, element, attribiutes) {


                        },
                        post: function ($scope, element, attribiutes) {
                            $scope.currentPhotoIndex = 0;

//                            console.log($scope.alloggio)
//                            console.log($scope.$parent)

                            $scope.buildAlloggioUrl = function(){
                                if ($scope.alloggio && $scope.alloggio.id)
                                    $scope.alloggio_url = djangoUrl.reverse('alloggio_detail',{pk:$scope.alloggio.id})

                            }
                            $scope.buildAlloggioUrl()

                            $scope.openAlloggioDetail = function($event){
                                $event.stopPropagation();
                                $event.preventDefault();
//                                console.log('openAlloggioDetail');
                                var url = djangoUrl.reverse('alloggio_detail',{pk:$scope.alloggio.id});

                                var params = {
                                    checkin: $scope.filters.checkin.date ? moment($scope.filters.checkin.date).format('YYYY-MM-DD HH:mm') : null ,
                                    checkout: $scope.filters.checkout.date ? moment($scope.filters.checkout.date).format('YYYY-MM-DD HH:mm'): null,
                                    numero_ospiti :$scope.filters.numero_ospiti,
                                }
                                for(var key in params) {
                                    if(! params[key]) {
                                        delete params[key];
                                    }
                                }


                                url  = url+'?'+$.param(params)
                                $window.location.href =url;

//                                console.log($.param({ a: [ 2, 3, 4 ] }))
//                                $location.path(url).search({
//                                    checkin: moment($scope.filters.checkin.date).format('YYYY-MM-DD HH:mm') ,
//                                    checkout: moment($scope.filters.checkout.date).format('YYYY-MM-DD HH:mm'),
//                                    numero_ospiti :$scope.filters.numero_ospiti,
//
//                                });

                            }




//                            function(){
//                                djangoUrl
//                                return 'djangoUrl'
//                            }

//                              $scope.$watch('filters',function(newValue, oldValue){
//                                if(newValue === oldValue){
//                                    return;
//                                  }
//                                console.log('update filters in alloggio preview')
//                                  $scope.buildAlloggioUrl()
////                                if ($scope.filters && $scope.filters.checkin && $scope.filters.checkin.date){
////                                    $location.search('checkin', $filter('date')($scope.filters.checkin.date, "yyyy-MM-dd HH:mm") );
////
////                                    if ($scope.filters && $scope.filters.checkout && $scope.filters.checkout.date)
////                                        $scope.updateSearch();
////                                }
//                            })



                            if ($scope.alloggio && typeof $scope.alloggio.gallery == 'string'){
                                $scope.alloggio.gallery = ApiGallery.get($scope.alloggio.gallery,function(){
//                                    console.log('Gallery get OK!!')
//                                    console.log($scope.alloggio.gallery)
//                                     $scope.currentImageSrc = $scope.alloggio.gallery.photos[0].thumbnail_url
                                });
                            }

                            $scope.currentImageSrc = function(){
//                                console.log(' get $scope.currentImageSrc ')
                                if ($scope.alloggio && $scope.alloggio.gallery && $scope.alloggio.gallery.photos && $scope.alloggio.gallery.photos.length > $scope.currentPhotoIndex )
                                    return $scope.alloggio.gallery.photos[$scope.currentPhotoIndex].thumbnail_url

                                return false
                            }

                            $scope.nextImage = function(event){
                                event.preventDefault();
                                event.stopPropagation();
                                if ($scope.currentPhotoIndex < $scope.alloggio.gallery.photos.length -1)
                                    $scope.currentPhotoIndex += 1;
                                else
                                    $scope.currentPhotoIndex = 0;
                            }
                            $scope.prevImage = function(event){
                                event.preventDefault();
                                event.stopPropagation();
                                if ($scope.currentPhotoIndex > 0)
                                    $scope.currentPhotoIndex -= 1;
                                else
                                    $scope.currentPhotoIndex = $scope.alloggio.gallery.photos.length -1;
                            }



//



                        }
                    }
                };
            }
        ]
    );

})(window.angular);
