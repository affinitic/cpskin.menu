$( document ).ready(function() {

    // Add 'activated' class to menu already loaded
    $('#portal-globalnav li.selected:not(#portaltab-index_html) a').addClass('activated');

    // Toggle between menu clicked
    var clickable_menu_selector = '#portal-globalnav li:not(#portaltab-index_html) a';
    $(clickable_menu_selector).each(function(){
        $(this).click(function() {

            var menu_id = this.parentNode.id.replace('portaltab-', '');
            var submenu = $('#portal-globalnav-cpskinmenu-' + menu_id);
            if (submenu.length === 0) {
                return true;
            }

            $(clickable_menu_selector).each(function(){
                $(this).removeClass('activated');
            });
            $(this).addClass('activated');

            $('ul.sf-menu').each(function(){
                $(this).hide();
            });
            submenu.show();
            return false;
        })
    });
});
