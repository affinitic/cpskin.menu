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

    function extract_submenu_children($elements, level){
        var $new_ul = $("<ul class='submenu submenu-active submenu-level-" + level + "' />");
        $elements.children('li').each(function(){
            var $children = $(this).find('> ul');
            var $new_li = $("<li />");
            var li_class = $children.length > 0 ? 'nofollow' : 'follow';
            $new_li.addClass(li_class)
                   .text($(this).find('> span > a').text().trim())
                   .data('referto', $(this).attr('id')).data('level', level);
            if (li_class == 'nofollow'){
                  // we have children and we need to open it in a new level menu
                  $new_li.on('click', function(){
                      var orig =  $('#'+$(this).data('referto').replace('.', '\\.'));
                      //remove all the collapsible siblings: next levels
                      $(this).parent().parent().siblings().remove();
                      //collapse the prev menu
                      $(this).parent().prev().click();
                      //create new levels
                      $('#advanced-breadcrumbs').append(create_menu_level(orig, $(this).data('level')+1));
                  });
            }
            else{
                $new_li.data('follow', $(this).find('span a').attr('href'));
                $new_li.on('click', function(){
                   location.href =  $(this).data('follow');
                });
                //we don't have children or we are in a level where we should follow the link
            }
            $new_ul.append($new_li);
        });
        return $new_ul;
    }

    function create_menu_level($element, level){
        var $new_level = $("<div class='advb-submenu' id='" + SUBMENU_PREFIX + level + "'/>");
        var $childrens = $element.find('> ul');
        //at most 4 level
        if (level<4){
            var $title = $("<div class='advb-title' id='" + ADVB_TITLE_PREFIX  + level +"' />")
                             .append($.trim($element.find('> span a').text()))
                             .on('click',
                                 function(){
                                     //open correct menu and close all other
                                     $(this).parent().siblings().click();
                                     $(this).parent().find('> ul').slideToggle()
                                                     .toggleClass('submenu-active');
                                 });
            $new_level.append($title);
            $new_level.append(extract_submenu_children($childrens, level));
            return $new_level;
            }
        return '';
    }

    function clone_first_level_menu($menu){
        /*
         * We create the collapsible menu cloning elements
         * */
        var $first_level = $menu.children('li');
        var $cloned_first_level = $first_level.clone();
        $cloned_first_level.find('> ul').remove();
        update_element_id($cloned_first_level, FL_PREFIX);
        $('#mobile-first-level-wrapper').append($("<ul class='mobile-first-level'/>").append($cloned_first_level));

    }
    function show_adv_breadcrumb($menu){
        /*
         * read from the menu structure le selected elements path and build collapsible breadcrumbs
         * */
        var $breadcrumbs = $menu.find('.navTreeItemInPath').add($menu.find('.selected').parent());
        //get all the li elements in the path and create the menu
        $($breadcrumbs).each(function(index, value){
            var element = $(value);
            $('#advanced-breadcrumbs').append(create_menu_level(element, index+1));
        })
        $('#advanced-breadcrumbs').find('div.advb-title').last().click();
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
            // n1: creo il menu a tendina
            clone_first_level_menu($menu);
            // n2: faccio le breadcrumbs
            show_adv_breadcrumb($menu);
        }
    });
})(jQuery);
