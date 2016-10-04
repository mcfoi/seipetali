/**
 * Created with PyCharm.
 * User: elfo
 * Date: 08/12/14
 * Time: 14:38
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with PyCharm.
 * User: elfo
 * Date: 05/12/14
 * Time: 14:51
 * To change this template use File | Settings | File Templates.
 */

(function (ng) {
    'use strict';
    var app = ng.module('angular-gallery', [])


//    app.directive('ngThumb', ['$window', function($window) {
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

    app.directive(
        'nggallery',
        [
            "$parse", '$http', '$timeout', 'FileUploader',
            function ($parse, $http, $timeout, FileUploader) {
                return {
                    restrict: 'AE',
//                    template: '<div> cacca </div>',
                    templateUrl: '/ng-template/gallery/angular-gallery.html',
//                    replace: true,
                    link: {pre: function ($scope, element, attribiutes) {



                        $scope.uploader = new FileUploader({
                            url: '/api/v1/photos/',
                            method: 'POST',
                            alias: 'image',
                            queueLimit: 8,
                            autoUpload: true,
                            removeAfterUpload: false,
                            headers: { 'Accept': '*/*' },
                        });

                        // FILTERS

                        $scope.uploader.filters.push({
                            name: 'customFilter',
                            fn: function (item /*{File|FileLikeObject}*/, options) {
                                return this.queue.length < 10;
                            }
                        });

                        // CALLBACKS

                        $scope.gallerySavePhotos = function(){
                            var photosUri = [];

                            angular.forEach($scope.gallery.photos, function(value, key) {
                              this.push(value.resource_uri);
                            }, photosUri);
//                            photosUri.push(response.resource_uri);

                            $http({
                                method: 'PATCH',
                                url: $scope.gallery.resource_uri,
                                data: {photos:photosUri}
//                                data: $scope.newCredit.person
                            }).success(function (result) {
                                    $scope.gallery = result;
                                    $scope.photos = $scope.gallery.photos
                            });
                        }

                        $scope.uploader.onWhenAddingFileFailed = function (item /*{File|FileLikeObject}*/, filter, options) {
                            console.info('onWhenAddingFileFailed', item, filter, options);
                        };
                        $scope.uploader.onAfterAddingFile = function (fileItem) {
                            console.info('onAfterAddingFile', fileItem);
                            $scope.generateThumb(fileItem._file)

                            fileItem.formData = [{
//                                foo:'bar',
//                                peppo:'franco'
                            }]

                        };
                        $scope.uploader.onAfterAddingAll = function (addedFileItems) {
                            console.info('onAfterAddingAll', addedFileItems);

                        };
                        $scope.uploader.onBeforeUploadItem = function (item) {
                            console.info('onBeforeUploadItem', item);
                        };
                        $scope.uploader.onProgressItem = function (fileItem, progress) {
                            console.info('onProgressItem', fileItem, progress);
                        };
                        $scope.uploader.onProgressAll = function (progress) {
                            console.info('onProgressAll', progress);
                        };
                        $scope.uploader.onSuccessItem = function (fileItem, response, status, headers) {
                            console.info('onSuccessItem', fileItem, response, status, headers);

                            $scope.gallery.photos.push(response);
                            $scope.gallerySavePhotos();



//                            $scope.gallery.photos.push(response);

                        };
                        $scope.uploader.onErrorItem = function (fileItem, response, status, headers) {
//                                console.info('onErrorItem', fileItem, response, status, headers);
                            console.info('onErrorItem', fileItem, status, headers);
                        };
                        $scope.uploader.onCancelItem = function (fileItem, response, status, headers) {
                            console.info('onCancelItem', fileItem, response, status, headers);
                        };
                        $scope.uploader.onCompleteItem = function (fileItem, response, status, headers) {
                            console.info('onCompleteItem', fileItem, response, status, headers);
                            console.info('onCompleteItem', fileItem, status, headers);
                        };
                        $scope.uploader.onCompleteAll = function () {
                            console.info('onCompleteAll');
                        };




                        $scope.dragControlListeners = {
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
                                $scope.gallerySavePhotos()
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
                            containment: '#gallery-sortable-container',
                            additionalPlaceholderClass: 'pull-left'
//                            containment: '#board'//optional param.
                        };


                    },
                        post: function ($scope, element, attribiutes) {


                             $scope.gallery = null;

                        console.log(attribiutes)

                        $scope.photos = [1,2,3,4,5]

                        if (attribiutes.galleryApiUrl){
                            $http({
                                    method: 'GET',
                                    url: attribiutes.galleryApiUrl,
        //                            params: $scope.newCredit.person,
    //                                data: $scope.newCredit.person

                                }).success(function (result) {
    //                                    console.log(result);
                                    $scope.gallery = result;
                                    $scope.photos = $scope.gallery.photos
    //                                    $scope.newCredit.person = result;
    //                                    $scope.addNewCredit();
                                    });
                            }else{
                                console.log('creo nuova gallery')
                                $http({
                                    method: 'POST',
                                    url: '/api/v1/gallerys/',
                                    data: {}
        //                            params: $scope.newCredit.person,
    //                                data: $scope.newCredit.person

                                }).success(function (result) {
    //                                    console.log(result);
                                        $scope.gallery = result;
                                        $scope.photos = $scope.gallery.photos
    //                                    $scope.newCredit.person = result;
    //                                    $scope.addNewCredit();
                                    });
                            }


                            console.log('init file uploader:')
                            console.log($scope.uploader)


//                        $scope.files = []
//                        $scope.usingFlash = FileAPI && FileAPI.upload != null;


                            $scope.fileReaderSupported = window.FileReader != null && (window.FileAPI == null || FileAPI.html5 != false);

//                        console.log(FileAPI);
                            console.log($scope.usingFlash);
                            console.log($scope.fileReaderSupported);


                            $scope.generateThumb = function (file) {
                                if (file != null) {
                                    if ($scope.fileReaderSupported && file.type.indexOf('image') > -1) {
                                        $timeout(function () {
                                            var fileReader = new FileReader();
                                            fileReader.readAsDataURL(file);
                                            fileReader.onload = function (e) {
                                                $timeout(function () {
                                                    file.dataUrl = e.target.result;
                                                });
                                            }
                                        });
                                    }
                                }
                            }


                            $scope.fileDropped = function ($files, $event, $rejectedFiles) {
                                console.log(' $scope.fileDropped', $files, $rejectedFiles)
                            }

//                        $scope.fileReaderSupported = window.FileReader != null && (window.FileAPI == null || FileAPI.html5 != false);

                            $scope.upload = function (files) {
                                console.log('$scope.upload', files)
                                $scope.formUpload = false;
                                if (files != null) {
                                    for (var i = 0; i < files.length; i++) {
                                        $scope.errorMsg = null;
                                        (function (file) {
                                            $scope.generateThumb(file);
                                            eval($scope.uploadScript);
                                        })(files[i]);
                                    }
                                }
//                            storeS3UploadConfigInLocalStore();
                            };


//                          $scope.$watch('files', function() {
//                                for (var i = 0; i < $scope.files.length; i++) {
//                                  var file = $scope.files[i];
//                                  $scope.upload = $upload.upload({
//                                    url: 'server/upload/url', // upload.php script, node.js route, or servlet url
//                                    //method: 'POST' or 'PUT',
//                                    //headers: {'Authorization': 'xxx'}, // only for html5
//                                    //withCredentials: true,
//                                    data: {myObj: $scope.myModelObj},
//                                    file: file, // single file or a list of files. list is only for html5
//                                    //fileName: 'doc.jpg' or ['1.jpg', '2.jpg', ...] // to modify the name of the file(s)
//                                    //fileFormDataName: myFile, // file formData name ('Content-Disposition'), server side request form name
//                                                                // could be a list of names for multiple files (html5). Default is 'file'
//                                    //formDataAppender: function(formData, key, val){}  // customize how data is added to the formData.
//                                                                                        // See #40#issuecomment-28612000 for sample code
//
//                                  }).progress(function(evt) {
//                                    console.log('progress: ' + parseInt(100.0 * evt.loaded / evt.total) + '% file :'+ evt.config.file.name);
//                                  }).success(function(data, status, headers, config) {
//                                    // file is uploaded successfully
//                                    console.log('file ' + config.file.name + 'is uploaded successfully. Response: ' + data);
//                                  });
//                                  //.error(...)
//                                  //.then(success, error, progress); // returns a promise that does NOT have progress/abort/xhr functions
//                                  //.xhr(function(xhr){xhr.upload.addEventListener(...)}) // access or attach event listeners to
//                                                                                          //the underlying XMLHttpRequest
//                                }
//                                /* alternative way of uploading, send the file binary with the file's content-type.
//                                   Could be used to upload files to CouchDB, imgur, etc... html5 FileReader is needed.
//                                   It could also be used to monitor the progress of a normal http post/put request.
//                                   Note that the whole file will be loaded in browser first so large files could crash the browser.
//                                   You should verify the file size before uploading with $upload.http().
//                                */
//                                // $scope.upload = $upload.http({...})  // See 88#issuecomment-31366487 for sample code.
//
//                              });


                        }}
                };
            }
        ]
    );

})(window.angular);