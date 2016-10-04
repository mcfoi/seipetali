/**
 * Created with PyCharm.
 * User: elfo
 * Date: 16/09/14
 * Time: 21:58
 * To change this template use File | Settings | File Templates.
 */

(function () {
'use strict';


angular.module('seipetali-app').config(function($animateProvider) {
  $animateProvider.classNameFilter(/angular-animate/);
})


angular.module('seipetali-app').config(function($locationProvider) {
  $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    }).hashPrefix('!');
})

//angular.module('seipetali-app').value('$sniffer', { history: true });




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
angular.module('seipetali-app').factory("ApiGallery", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'gallerys'}),
        cache: false
    });
}]);
angular.module('seipetali-app').factory("ApiReservation", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'reservation'}),
        cache: false
    });
}]);
angular.module('seipetali-app').factory("ApiPayment", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'payment'}),
        cache: false
    });
}]);
angular.module('seipetali-app').factory("ApiUser", ["TastyResource",'djangoUrl', function (TastyResource,djangoUrl) {
    return TastyResource({
        url: djangoUrl.reverse('api_dispatch_list',{api_name:'v1',resource_name:'user'}),
        cache: false
    });
}]);


angular.module('ui.bootstrap').directive('datepickerPopup', function (dateFilter, datepickerPopupConfig) {
  return {
    restrict: 'A',
    priority: 1,
    require: 'ngModel',
    link: function(scope, element, attr, ngModel) {
      var dateFormat = attr.datepickerPopup || datepickerPopupConfig.datepickerPopup;
      ngModel.$formatters.push(function (value) {
        return dateFilter(value, dateFormat);
//          console.log(value,typeof value,moment(value))
//          var momentDate = moment(value)
//          console.log(momentDate.format('MMMM'));
//          return 'dicembre'
//        return moment(value).format('MMMM')
      });
    }
  };
});


/*
 * Creates a range
 * Usage example: <option ng-repeat="y in [] | range:1998:1900">{{y}}</option>
 */
angular.module('seipetali-app').filter('range', function() {
  return function(input, start, end) {
    start = parseInt(start);
    end = parseInt(end);
    var direction = (start <= end) ? 1 : -1;
    while (start != end) {
        input.push(start);
        start += direction;
    }
    return input;
  };
});

angular.module('seipetali-app').factory('jQuery', [
        '$window',
        function ($window) {
            return $window.jQuery;
        }
    ]);




})();

angular.module('seipetali-app').directive('smartFloat', function ($filter) {
    var FLOAT_REGEXP_1 = /^\$?\d+.(\d{3})*(\,\d*)$/; //Numbers like: 1.123,56
    var FLOAT_REGEXP_2 = /^\$?\d+,(\d{3})*(\.\d*)$/; //Numbers like: 1,123.56
    var FLOAT_REGEXP_3 = /^\$?\d+(\.\d*)?$/; //Numbers like: 1123.56
    var FLOAT_REGEXP_4 = /^\$?\d+(\,\d*)?$/; //Numbers like: 1123,56

    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (viewValue) {
                if (FLOAT_REGEXP_1.test(viewValue)) {
                    ctrl.$setValidity('float', true);
                    return parseFloat(viewValue.replace('.', '').replace(',', '.'));
                } else if (FLOAT_REGEXP_2.test(viewValue)) {
                        ctrl.$setValidity('float', true);
                        return parseFloat(viewValue.replace(',', ''));
                } else if (FLOAT_REGEXP_3.test(viewValue)) {
                        ctrl.$setValidity('float', true);
                        return parseFloat(viewValue);
                } else if (FLOAT_REGEXP_4.test(viewValue)) {
                        ctrl.$setValidity('float', true);
                        return parseFloat(viewValue.replace(',', '.'));
                }else {
                    ctrl.$setValidity('float', false);
                    return undefined;
                }
            });

            ctrl.$formatters.unshift(
               function (modelValue) {
                   return $filter('number')(parseFloat(modelValue) , 2);
               }
           );
        }
    };
});




