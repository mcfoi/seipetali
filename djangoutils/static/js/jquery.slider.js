(function($){
  $.fn.slider = function(url, options) {

    var settings = {
      form_selector: null,
      activate: null,
      rpp: 10
    };

    return this.each(function() {

      if(options) {
        $.extend(settings, options);
      }

      // Declare a function to load content.
      function loadContent(carousel, state) {

	// Do we already have this page? If so, return.
	if(carousel.has(carousel.first)) {
	  return;
	}

	carousel.lock();

	// Do we have any form data?
	var form_data = carousel.options.form_data;
	if(!form_data) {
	  form_data = new Array();
	}
	else {
	  // Clone to avoid repeated 'page' and 'rpp' entries.
	  form_data = form_data.slice(0);
	}

	// Add the pagination details.
	form_data.push({'name': 'page', 'value': carousel.first});
	form_data.push({'name': 'rpp', 'value': settings.rpp}); // results per page

	// Ajax call.
	$.get(url, $.param(form_data), function(data) {
	  carousel.size(data.num_pages);
	  page = carousel.add(carousel.first, '<div><ul>' + data.page + '</ul></div>');
	  if(settings.activate) {
	    settings.activate(page);
	  }
	  carousel.unlock();
	});

	// Free previous page.
	if(carousel.prevFirst != null) {
	  carousel.remove(carousel.prevFirst);
	}

      }

      // Setup the carousel.
      opts = {
	scroll: 1,
	itemLoadCallback: loadContent
      }
      if(settings.form_selector) {
	opts.form_data = $(settings.form_selector).serializeArray()
      }
      $(this).jcarousel(opts);
      var cr = $(this).data('jcarousel');
      $('.jcarousel-next').html('<a href="javascript:void();" class="show-result">NEXT PAGE</a>');
      $('.jcarousel-prev').html('<a href="javascript:void();" class="show-result">PREVIOUS PAGE</a>');

      // Setup the form to submit values to me.
      if(settings.form_selector) {
	$(settings.form_selector).submit(function() {
	  cr.options.form_data = $(this).serializeArray();
	  cr.reset();
	  return false;
	});
      }

    });

  }
})( jQuery );
