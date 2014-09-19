$( document ).ready(function() {
    $('#portal-globalnav li:not(.menutools-item):not(#portaltab-index_html) a').each(function(){
        $(this).click(function() {
            var menu_id = this.parentNode.id.replace('portaltab-', '');
            jQuery('#portal-globalnav-cpskinmenu-' + menu_id).toggle();
            return false;
        })
    });
});
