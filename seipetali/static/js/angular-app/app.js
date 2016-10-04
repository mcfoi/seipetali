/**
 * Created with PyCharm.
 * User: elfo
 * Date: 16/09/14
 * Time: 21:58
 * To change this template use File | Settings | File Templates.
 */

(function () {
'use strict';

angular.module('seipetali-app', [   'ngRoute',
                                    'ngAnimate',
                                    'ngResource',
                                    'tastyResource',
                                    'angularFileUpload',
                                    'angular-address',
                                    'angular-gallery',
                                    'angular-optional-services',
                                    'angular-alloggio-search',
                                    'angular-alloggio-calendar',
                                    'uiGmapgoogle-maps',
                                    'siyfion.sfTypeahead',
                                    'ui.sortable',
                                    'ng.django.urls',
                                    'ui.bootstrap',
                                    'ui.calendar',
                                    ])


angular.module('seipetali-app').config(function($animateProvider) {
  $animateProvider.classNameFilter(/angular-animate/);
})


angular.module('seipetali-app').config(function($locationProvider) {
  $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
})




//angular.module('seipetali-app').config(['$resourceProvider', function($resourceProvider) {
//  // Don't strip trailing slashes from calculated URLs
//  $resourceProvider.defaults.stripTrailingSlashes = false;
//}]);



//Set Tastypie resource

angular.module('seipetali-app').factory("ApiIva", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'ivas'}),
        cache: false
    });
}]);

angular.module('seipetali-app').factory("ApiServizioOpzionale", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'servizioopzionale'}),
        cache: false
    });
}]);

angular.module('seipetali-app').factory("ApiServizioBase", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'serviziobase'}),
        cache: false
    });
}]);

angular.module('seipetali-app').factory("ApiAlloggio", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'alloggio'}),
        cache: false
    });
}]);
angular.module('seipetali-app').factory("ApiEvent", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'event'}),
        cache: false
    });
}]);
angular.module('seipetali-app').factory("ApiCalendar", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'calendar'}),
        cache: false
    });
}]);



//// Initialize the main module
//angular.module('collateralfilms-app').run(['$rootScope', '$location', '$window', function ($rootScope, $location, $window) {
//
//    'use strict';
//
//    /**
//     * Helper method for main page transitions. Useful for specifying a new page partial and an arbitrary transition.
//     * @param  {String} path               The root-relative url for the new route
//     * @param  {String} pageAnimationClass A classname defining the desired page transition
//     */
//    $rootScope.go = function (path, pageAnimationClass) {
//
//        console.log('Go',pageAnimationClass)
//
//        if (typeof(pageAnimationClass) === 'undefined') { // Use a default, your choice
//            $rootScope.pageAnimationClass = 'crossFade';
//        }
//
//        else { // Use the specified animation
//            $rootScope.pageAnimationClass = pageAnimationClass;
//        }
//
//        if (path === 'back') { // Allow a 'back' keyword to go to previous page
//            $window.history.back();
//        }
//
//        else { // Go to the specified path
//            $location.path(path);
//        }
//    };
//}]);
})();


//
//(function(){
//    'use strict';
//
//
//angular
//
//
//    .module('collateralfilms-app')
//
//
//    // Angular File Upload module does not include this directive
//    // Only for example
//
//
//    /**
//    * The ng-thumb directive
//    * @author: nerv
//    * @version: 0.1.2, 2014-01-09
//    */
//    .directive('ngThumb', ['$window', function($window) {
//        var helper = {
//            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
//            isFile: function(item) {
//                return angular.isObject(item) && item instanceof $window.File;
//            },
//            isImage: function(file) {
//                var type =  '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
//                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
//            }
//        };
//
//        return {
//            restrict: 'A',
//            template: '<canvas/>',
//            link: function(scope, element, attributes) {
//                if (!helper.support) return;
//
//                var params = scope.$eval(attributes.ngThumb);
//
//                if (!helper.isFile(params.file)) return;
//                if (!helper.isImage(params.file)) return;
//
//                var canvas = element.find('canvas');
//                var reader = new FileReader();
//
//                reader.onload = onLoadFile;
//                reader.readAsDataURL(params.file);
//
//                function onLoadFile(event) {
//                    var img = new Image();
//                    img.onload = onLoadImage;
//                    img.src = event.target.result;
//                }
//
//                function onLoadImage() {
//                    var width = params.width || this.width / this.height * params.height;
//                    var height = params.height || this.height / this.width * params.width;
//                    canvas.attr({ width: width, height: height });
//                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
//                }
//            }
//        };
//    }]);
//
//})();
//


