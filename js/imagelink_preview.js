/*
 * Image URL preview script
 * powered by jQuery (http://www.jquery.com)
 *
 * Adapted from a script by Alen Grakalic (http://cssglobe.com) for better
 * compatibility with a specific Jekyll/Markdown use case.
 *
 * for more info visit http://cssglobe.com/post/1695/easiest-tooltip-and-image-preview-using-jquery
 *
 * TODO: Fix the `top_val` calculation so it's re-run after initial image load
 *       resizes the popup.
 */

$(document).ready(function(){
	// these 2 variable determine popup's distance from the cursor
	// you might want to adjust to get the right result
	var xOffset = 20;
	var yOffset = 5;


	$("a[href$='.jpg'], a[href$='.jpeg'], a[href$='.png']").each(function() {
		var $this = $(this);
		var popup;

		var movePopup = function(e) {
			var top_val = Math.min(
					e.pageY + yOffset,
					(window.pageYOffset + window.innerHeight) - popup.height() - 20
				);
			popup.css({
				position: 'absolute',
				top: top_val + "px",
				left: (e.pageX + xOffset) + "px"
			});
		};

		$this.hover(function(e) {
			var img = $("<img alt='url preview' />").attr('src', this.href);
			var caption = $("<p class='caption'></p>").text($this.text());
			popup = $("<div></div>").addClass("url_preview")
				.append(img)
				.append(caption)
				.appendTo("body");
			movePopup(e);
		},
		function(){
			popup.remove();
		}).mousemove(movePopup)
		.attr('title', null)
		.css({
			color: 'black',
			textDecoration: 'none',
			borderBottom: '1px dotted'
		});
	});
});
