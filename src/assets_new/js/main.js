$(document).ready(function() {
	
	/***************************** To center Modal ENDs ***************************************/
				
				var modalVerticalCenterClass = ".modal";
				
				function centerModals($element) {
					var $modals;
					if ($element.length) {
						$modals = $element;
					} else {
						$modals = $(modalVerticalCenterClass + ':visible');
					}
					$modals.each( function(i) {
						var $clone = $(this).clone().css('display', 'block').appendTo('body');
						var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
						top = top > 0 ? top : 0;
						$clone.remove();
						$(this).find('.modal-content').css("margin-top", top);
					});
				}
				$(modalVerticalCenterClass).on('show.bs.modal', function(e) {centerModals($(this));});
				$(window).on('resize', centerModals);
				
		/***************************** To center Modal ENDs ***************************************/
		
		
		/***************************** To hide page data for sidebar on mobile  ********************/
		
				if($( window ).width() <= 767) {

					$( "#menu-toggle-2" ).click(function() {
						var toggle = $( "#wrapper" ).hasClass("toggled");
							
						if(toggle == false){
							$('#page-content-wrapper').css('display','block');
									
						} else {
							$('#page-content-wrapper').css('display','none');
						}
						
					});
				}
		/***************************** To hide page data for sidebar on mobile ENDS ********************/
});