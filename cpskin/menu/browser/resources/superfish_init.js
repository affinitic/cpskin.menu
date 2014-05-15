/* initialise plugins */
;(function($){
    "use strict";

    var FL_PREFIX = 'first-level-';
    var SUBMENU_PREFIX = 'advb-submenu-level-';
    var ADVB_TITLE_PREFIX = 'title-level-';

    function update_element_id($elements, PREFIX){
         $elements.each(function(index, value){
            var element = $(value);
            var new_id = PREFIX + element.attr('id');
            element.attr('id', new_id);
        })
    }

    function create_menu_level($element, level){
        var new_level = $("<div id='" + SUBMENU_PREFIX + level + "'/>");
        var childrens = $element.find('> ul');
        if (childrens.length > 0){
            var title = $.trim($element.find('> span a').text()).wrap("<div class='advb-title' id='" + ADVB_TITLE_PREFIX  + level +"' />");
            new_level.append(title);
            //new_level.append();

        }
        $('#advanced-breadcrumbs').append(new_level);
    }

    function clone_first_level_menu($menu){
        var $first_level = $menu.children('li');
        var $cloned_first_level = $first_level.clone();
        $cloned_first_level.find('> ul').remove();
        update_element_id($cloned_first_level, FL_PREFIX);
        $('#mobile-first-level-wrapper').append($("<ul class='mobile-first-level'/>").append($cloned_first_level));

    }
    function show_adv_breadcrumb($menu){
        var $breadcrumbs = $menu.find('.navTreeItemInPath').extend($menu.find('.selected').parent()).get().reverse();
        $($breadcrumbs).each(function(index, value){
            var element = $(value);
            var new_level = create_menu_level(element, index+1);
        })
    }

    $( document ).ready(function() {
        var $isMobile = Detectizr.device.type == 'mobile';
        if (!$isMobile){
            $('ul.sf-menu').superfish();
        }
        else{
            var $menu = $('#portal-globalnav-cpskinmenu-mobile');
            $('#mobnav-btn').on('click',
                                function(){
                                   $('#mobile-first-level-wrapper').slideToggle()
                                                                   .toggleClass('menu-active');
                                   });
            clone_first_level_menu($menu);
            show_adv_breadcrumb($menu);
        }
    });
})(jQuery);
