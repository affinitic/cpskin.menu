$( document ).ready(function() {

    // Add 'activated' class to menu already loaded
    $('#portal-globalnav li.selected:not(.menutools-item):not(#portaltab-index_html)').addClass('activated');

    // Toggle between menu clicked
    var clickable_menu_selector = '#portal-globalnav li:not(.menutools-item):not(#portaltab-index_html) a';
    $(clickable_menu_selector).each(function(){
        $(this).click(function() {

            $(clickable_menu_selector).each(function(){
                $(this).removeClass('activated');
            });
            $(this).addClass('activated');

            $('ul.sf-menu').each(function(){
                $(this).hide();
            });
            var menu_id = this.parentNode.id.replace('portaltab-', '');
            jQuery('#portal-globalnav-cpskinmenu-' + menu_id).show();
            return false;
        })
    });
});
