/* initialise plugins */
;(function($){
    "use strict";
    $( document ).ready(function() {
        var $isMobile = Detectizr.device.type == 'mobile';
        if (!$isMobile){
            $('ul.sf-menu').superfish();
        }
        else{
            var $$ = $('ul.sf-menu');
            var $liHasUl = $$.find('li:has(ul)');
            var $mobileArrow = $('<div class="mobnav-subarrow"></div>');
            $liHasUl.find('> span').after($mobileArrow.clone());

            $('#mobnav-btn').click(
                function () {
                    $('.sf-menu').toggleClass("xactive");
                });
            $('.mobnav-subarrow').click(
                function () {
                    $(this).parent().toggleClass("xpopdrop");
                });
        }
    });
})(jQuery);
