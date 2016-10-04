(function($){
  $.fn.inner_label = function() {

    return this.each(function() {

      $(this).blur(function() {
        if(this.value == '') {
          this.value = this.name.toUpperCase();
        }
      }).focus(function() {
        if(this.value == this.name.toUpperCase()) {
          this.value = '';
        }
      }).click(function() {
        if(this.value == this.name.toUpperCase()) {
          this.value = '';
        }
      }).blur();

    });

  };
})( jQuery );

(function($){
  $.fn.inner_label_clear = function() {

    return this.each(function() {

      if(this.value == this.name.toUpperCase()) {
        this.value = '';
      }

    });

  };
})( jQuery );

(function($){
  $.fn.show_map = function(options) {

    var settings = {
      height: null,
      depth: 16,
      latitude: null,
      longitude: null,
      marker_html: null
    };

    return this.each(function() {

      if(options) {
        $.extend(settings, options);
      }

      var map_marker = $('#show-map-marker');
      if(!map_marker.length) {
        $('body').append('<div id="show-map-marker"></div>');
        map_marker = $('#show-map-marker');
      }

      var map_options = {};
      if(settings.marker_html != null) {
        map_marker.html(settings.marker_html);
        map_options.markers = {
          info: {
            layer: '#show-map-marker',
            popup: true
          }
        };
      }
      if(settings.latitude != null && settings.longitude != null) {
        map_options.latitude = settings.latitude;
        map_options.longitude = settings.longitude;
        map_options.markers.latitude = settings.latitude;
        map_options.markers.longitude = settings.longitude;
      }

      if(settings.height) {
        $(this).height(settings.height);
      }
      $(this).googleMaps(map_options);
    });

  };
})( jQuery );

// BROKEN, NEEDS WORK
(function($){
  $.fn.ajax_scrollpane = function(url, options) {

    var settings = {
      form: null,
      page: 1,
      page_size: 10,
      success: null
    };

    return this.each(function() {

      if(options) {
        $.extend(settings, options);
      }

      // Setup the jScrollPane.
      var jsp_api = $(this).jScrollPane(options).data('jsp');
      var pane = jsp_api.getContentPane();

      // Is this our first call?
      var data = $(this).data('ajsp');
      if(!data) {
        pane.append('<div id="ajsp-block-a" style="padding:0;margin:0;"></div>');
        pane.append('<div id="ajsp-block-b" style="padding:0;margin:0;"></div>');
        $(this).data('ajsp', {
          block_a: pane.find('#ajsp-block-a'),
          block_b: pane.find('#ajsp-block-b'),
		    page: settings.page,
		    locked: false
        });
        data = $(this).data('ajsp');
      }

      // Cache some data.
      var block_a = data.block_a;
      var block_b = data.block_b;

      // Begin loading initial content.
      block_a.load(url, $.param({'page': data.page, 'rpp': settings.page_size}), function() {
        if(settings.success) {
          settings.success(block_a);
        }
	// var pane_height = block_a.children().outerHeight(true);
        // block_a.height(pane_height);
        jsp_api.reinitialise();
      });
      block_b.load(url, $.param({'page': data.page + 1, 'rpp': settings.page_size}), function() {
        if(settings.success) {
          settings.success(block_b);
        }
	// var pane_height = block_b.children().outerHeight(true);
        // block_b.height(pane_height);
        jsp_api.reinitialise();
      });
      $(this).data('ajsp', {'page': data.page + 1});

      $(this).bind('jsp-arrow-change', function(event, isAtTop, isAtBottom, isAtLeft, isAtRight) {
        data = $(this).data('ajsp');
        if(isAtBottom && !data.locked) {
          data.locked = true;
	  block_a.html(block_b.html());
	  block_b.empty();
	  jsp_api.reinitialise();
          data.page += 1;
          block_b.load(url, $.param({'page': data.page, 'rpp': settings.page_size}), function() {
	    if(settings.success) {
              settings.success(block_b);
            }
            jsp_api.reinitialise();
            data.locked = false;
          });
        }
        else if(isAtTop && !data.locked) {
          data.locked = true;
          block_b.html(block_a.html());
          block_a.empty();
	  //jsp_api.reinitialise();
	  data.page -= 1;
          block_a.load(url, $.param({'page': data.page, 'rpp': settings.page_size}), function() {
	    if(settings.success) {
              settings.success(block_a);
            }
            jsp_api.reinitialise();
            data.locked = false;
          });
        }
      });

    });

  };
})( jQuery );
