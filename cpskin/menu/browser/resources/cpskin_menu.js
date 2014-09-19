$( document ).ready(function() {

    $('#portal-globalnav li:not(.menutools-item):not(#portaltab-index_html) a').each(function(){
        $(this).click(function() {

            $('ul.sf-menu').each(function(){
                $(this).hide();
            });

            var menu_id = this.parentNode.id.replace('portaltab-', '');
            jQuery('#portal-globalnav-cpskinmenu-' + menu_id).show();
            return false;
        })
    });
});
