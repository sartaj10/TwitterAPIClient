function getDocHeight() {
	var D = document;
	return Math.max(
		D.body.scrollHeight, D.documentElement.scrollHeight,
		D.body.offsetHeight, D.documentElement.offsetHeight,
		D.body.clientHeight, D.documentElement.clientHeight
	);
}

$(document).ready(() => {

	var ajax_call_sent = false;

	$(window).scroll(() => {
		
		if(!ajax_call_sent && $(window).scrollTop() + $(window).height() == getDocHeight()) {
			if($('#next_id').length) {
				var next_results = $('#next_id').val();
				ajax_call_sent = true;
				var encoded_data = {};
				encoded_data.next_results = next_results;

				$('.loader_gif').html('<img src="https://gadgets360.com/shop/static/web/images/loading_icon_small.gif">');

				$.ajax({
					type: "GET",
					url: "/getMoreTweets",
					data: { next_results : next_results },
					cache: false,
					success: function( response ) {
						$('.loader_gif').html('');
						var data = JSON.parse(response);

						if( data["status"] == 200 ){
							// append the new tweets at the end
							$('#all-results').append( data["html"] );
							// put new max_id into the same hidden field
							$('#next_id').val( data["new_next_results"] );
						}
						else if( data["status"] == 400 ){
							// show error text
							$('.loader_gif').html('<p>Error fetching tweets. Please try again.</p>');
						}

						// unset the flag to let the dom call another ajax call when reached bottom
						ajax_call_sent = false;
					},

					/**
					 * error() - callback function if there is an error in AJAX request
					 */
					error: function() {
						// hide loading image, and show error text
						$('.loader_gif').html('<p>Error fetching tweets. Please try again.</p>');
						// unset the flag to let the dom call another ajax call when reached bottom
						ajax_call_sent = false;
					}
				});
			}
			else {
				$('.loader_gif').html('<p>Error fetching tweets. Please try again.</p>');
			}
		}
	});
});
