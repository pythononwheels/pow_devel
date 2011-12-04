$( document ).ready( function(){
	$('.slides ul').jcarousel({
		scroll: 1,
		wrap: 'both',
		/* auto: 6,*/
		initCallback: _init_carousel,
		itemFirstInCallback:_first_callback,
		buttonNextHTML: null,
		buttonPrevHTML: null
	});
	
	$('#navigation li').hover(
		function(){ $(this).find('a').addClass('hover') },
		function(){ $(this).find('a').removeClass('hover') }
	);
});

function _init_carousel(carousel) {
	$('#slider-navigation a').bind('click', function() {
		var index = $(this).parent().parent().find('a').index(this) + 1;
		carousel.scroll( index );
		return false;
	});
};

function _first_callback(carousel, item, idx, state) {
	var index = idx - 1;
	$('#slider-navigation a').removeClass('active');
	$('#slider-navigation a').eq(index).addClass('active');
};