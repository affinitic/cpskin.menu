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

    function extract_submenu_children($elements, level, createdby){
        var $new_ul = $("<ul class='submenu submenu-level-" + level + "' />");
        $elements.children('li').each(function(index, value){
            var $children = $(this).find('> ul');
            var $new_li = $("<li />");
            var li_class = $children.length > 0 ? 'nofollow' : 'follow';
            var selected = '';
            if ($(this).find('> span').hasClass('selected')){
                selected = 'selected';
            }
            $new_li.addClass(li_class)
                   .addClass(selected)
                   .text($(this).find('> span > a').text().trim())
                   .data('referto', $(this).attr('id'))
                   .data('level', level)
                   .data('orig_id', $(this).attr('id'));

            //if we have link or level is greater than 1 follow the link
            if(li_class=='follow' || level > 2){
                //we don't have children or we are in a level where we should follow the link
                $new_li.data('follow', $(this).find('span a').attr('href'));
                $new_li.on('click', function(){
                   location.href =  $(this).data('follow');
                });
            }
            else{
                  // we have children and we need to open it in a new level menu
                  $new_li.on('click', function(){
                      //var orig =  $('#'+$(this).data('referto').replace('.', '\\.'));
                      var orig = $('#'+$(this).data('referto').replace( /(:|\.|\[|\])/g, "\\$1" ))
                      //remove all the collapsible siblings: next levels
                      //but let's prevent to remove nextMenu if we select an already opened
                      var orig_id = $(this).data('orig_id');
                      var remove = true;

                      // check if we already have this menu in breadcrumbs
                      var $others_menu = $(this).parent().parent().nextAll();
                      $others_menu.each(function(){
                          if ($(this).data('orig_id') == orig_id)
                              remove = false;
                              return false;
                      })
                      // in any case, collapse the actual menu
                      $(this).parent().prev().click();
                      //if not, remove all next menu and update breadcrumbs if yes open correct menu
                      if (remove){
                          $(this).parent().parent().nextAll().remove();
                          //create new levels
                          $('#advanced-breadcrumbs').append(create_menu_level(orig, $(this).data('level')+1, 'click'));}
                      else{
                          //need to open the next menu
                          $others_menu.each(function(){
                              if ($(this).data('orig_id') == orig_id)
                                  $(this).find('> span').click();
                          })
                      }
                  });
            }
            $new_ul.append($new_li);
        });
        if (createdby  == 'click')
            $new_ul.css({'display':'block'}).addClass('submenu-active');
        return $new_ul.children().length > 0 ? $new_ul : '';
    }

    function create_menu_level($element, level, createdby){
        var $new_level = $("<div class='advb-submenu' id='" + SUBMENU_PREFIX + level + "'/>")
                         .data('orig_id', $element.attr('id'));
        //console.log("id di menu: " +  $element.attr('id'))
        //$new_level.data('original_element_id', $element.attr('id'));
        var $childrens = $element.find('> ul');
        //at most 4 level
        if (level<4){
            var selected = '';
            if ($element.find('> span').hasClass('selected')){
                selected = 'selected';
            }
            var $title = $("<span class='advb-title' id='" + ADVB_TITLE_PREFIX  + level +"' />")
                  .addClass(selected)
                  .append($.trim($element.find('> span a').text()))
                  .on('click',
                      function(){
                          //open correct menu and close the others
                          $(this).parent().siblings().each(function(){
                              if($(this).children('ul').is(':visible'))
                                  $(this).children('ul').slideUp().removeClass('submenu-active');
                          })
                          $(this).parent().find('> ul').slideToggle()
                                          .toggleClass('submenu-active');
                      });
            $new_level.append($title);
            $new_level.append(extract_submenu_children($childrens, level, createdby));
            return $new_level;
            }
        return '';
    }

    function create_first_level_menu($menu){
        /*
         * We create the collapsible menu cloning elements
         * */
        var $first_level = $menu.children('li');
        var $cloned_first_level = $first_level.clone();
        $cloned_first_level.find('> ul').remove();
        update_element_id($cloned_first_level, FL_PREFIX);
        $('#mobile-first-level-wrapper').append($("<ul class='mobile-first-level'/>").append($cloned_first_level));

    }
    function create_breadcrumb($menu){
        /*
         * read from the menu structure le selected elements path and build collapsible breadcrumbs
         * */
        var $breadcrumbs = $menu.find('.navTreeItemInPath');
        //add selected element to bc only if it's a list
        if($menu.find('.selected').parent().find('> ul').length > 0){
            var $breadcrumbs = $menu.find('.navTreeItemInPath').add($menu.find('.selected').parent());
        }
        else{
            var $breadcrumbs = $menu.find('.navTreeItemInPath');
        }
        //get all the li elements in the path and create the menu
        $($breadcrumbs).each(function(index, value){
            var element = $(value);
            $('#advanced-breadcrumbs').append(create_menu_level(element, index+1, 'breadcrumbs'));
        })
        $('#advanced-breadcrumbs').find('div ul').not(':last').hide();
    }

    $( document ).ready(function() {
        //initialize superfish
        $('ul.sf-menu').superfish();

        //initialize drop down menu
        var $menu = $('#portal-globalnav-cpskinmenu-mobile');
        $('#mobnav-btn').on('click',
                            function(){
                               $('#mobile-first-level-wrapper').slideToggle()
                                                               .toggleClass('menu-active');
                               });
        //first: create first level menu
        create_first_level_menu($menu);
        //second: create breadcrumbs
        create_breadcrumb($menu);

        $('#search-btn').prepOverlay(
            {
                subtype: 'ajax',
                filter: '#portal-searchbox',
                config: {expose:{color:'#00f'}},
                cssclass: 'mobile-overlay-search'
            }
        );
    });
})(jQuery);
