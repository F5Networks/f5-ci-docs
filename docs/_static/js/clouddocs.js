// Use the header and footer from the current host (clouddocs.f5.com or clouddocs.f5networks.net)
$(document).ready(function () {
    var loc = window.location,
    host = loc.protocol + '//' + loc.host;
    $('#clouddocs-header').load(host + './header.html', loadCoveoComponents);
    $('#clouddocs-footer').load(host + './footer.html');

    Coveo.SearchEndpoint.configureCloudV2Endpoint('', 'xx564559b1-0045-48e1-953c-3addd1ee4457');
});

// Callback function that runs after loading the header component into the page
function loadCoveoComponents() {
  var root = Coveo.$$(document).find('#searchbox');
  Coveo.initSearchbox(root, 'https://support.f5.com/csp/federated-search');

  // Show search bar and hide search toggle button if on index page
  var path = window.location.pathname;
  if (path == '/' || path == '/index.html') {
    hideSearchToggleBtn();
    showSearchBar();
  }
  
  // Event listener for click on search toggle button
  document.getElementById('search-toggle').addEventListener('click', function() {
    var searchContainer = document.getElementById('search-container');
    var isVisible = searchContainer.style.overflow === 'visible';
    // Toggle visibility
    if (isVisible) {
      hideSearchBar(); 
    } else {
      showSearchBar();
    }
  })
}

// Show Coveo search bar
function showSearchBar() {
  var searchContainer = document.getElementById('search-container');
  searchContainer.style.overflow = 'visible';
  searchContainer.style.height = 'auto';
}

// Hide Coveo search bar
function hideSearchBar() {
  var searchContainer = document.getElementById('search-container');
  searchContainer.style.overflow = 'hidden';
  searchContainer.style.height = '0px';
}

// Hide search toggle button in the header
function hideSearchToggleBtn() {
  var button = document.getElementById('search-toggle');
  button.style.display = 'none';
}

// collapsible sidebar
$(document).ready(function () {

    $('#sidebarCollapse, #dismiss').on('click', function () {
        $('#sidebar').toggleClass('active');
        $('#content').toggleClass('active');
    });

    //Used to check that the megamenu exists. When user hovers over menu, changes z-index of TOC so
    //it does not overlap the megamenu
    var checkExist = setInterval(function() {
       if ($('#MainMenu').length) {
         $("#MainMenu").hover(function(){
           $('#sidebar').css("z-index", "-1");
           }, function(){
           $('#sidebar').css("z-index", "0");
         });
        clearInterval(checkExist);
       }
    }, 500); // check every 500ms

});

// Function to resize the sidebar if the footer covers it
function resizeScrollbar() {
  //Set the max heigh as either the content max height or the css max-height property
  var contentHeight = 0;
  if ($(".nav-sidebartoc").height() < parseInt($("#sidebar").css('max-height'))) {
    contentHeight = $(".nav-sidebartoc").height();
  }else {
    contentHeight = $("#sidebar").css('max-height');
  }
  contentHeight = parseInt(contentHeight);

  //get the sidebar bottom offset and the footer top offset
  var sidebarBottom = $("#sidebar").offset().top + $("#sidebar").outerHeight(true) - 25;
  var footerTop = $("#clouddocs-footer").offset().top;

  //if checks if there is a collision, if so then shrink the sidebar
  if (sidebarBottom >= footerTop) {
    var shorterNewHeight = $("#sidebar").height() - (sidebarBottom - footerTop) - 40;
    $("#sidebar").height(shorterNewHeight);

  //checks if the footer has moved away, so the sidebar needs to grow back
  }else if($("#sidebar").height() < contentHeight) {
    var tallerNewHeight = $("#sidebar").height() + (footerTop - sidebarBottom) - 40;
    if (tallerNewHeight > contentHeight) {
      $("#sidebar").height(contentHeight + 40);
    }else {
      $("#sidebar").height(tallerNewHeight);
    }
  }

  if($("#sidebar").height() < 140) {
    console.log("height is too short!");
    $("#sidebar").height(160);
  }
}

//Calls sidebar resize function on page load and when there is scrolling
$(document).ready(function () {

  /* JavaScript Media Queries, check if mobile view and do not resize TOC */
  if (matchMedia) {
  	const mq = window.matchMedia("(max-width: 768px)");
  	mq.addListener(WidthChange);
  	WidthChange(mq);
  }

  // Checks if resize TOC should be called when page is resized
  function WidthChange(mq) {
  	if (!mq.matches) {
      console.log("im resizing the TOC");
  	  resizeScrollbar();
  	}
  }

  //Throttle for scroll
  $(window).scroll(function() {
  clearTimeout($.data(this, 'scrollTimer'));
    $.data(this, 'scrollTimer', setTimeout(function() {
      resizeScrollbar();
  }, 250));
  });
});

  //collapse/show sidebar toc content
  $(document).ready(function () {

    //find the right li element, check if they have a ul and content, and add the button
    $('.nav-sidebartoc li').has('ul').each(function(index) {
      if ($(this).children('ul').children('li').length >= 1) {
        var $btn = $('<i/>', {
            class: 'collapseButton fa fa-caret-down',
        })
        $(this).prepend($btn);
        $(this).addClass("nestedList");
      }
    });

    //when the button is clicked do this
    $('.collapseButton').click(function() {
      var el = $(this);

      //hide/show the ul
      el.siblings('ul').slideToggle();

      //check what text the button has and change class appropriately (-/+)
      if (el.hasClass('fa-caret-down')) {
        el.removeClass('fa-caret-down').addClass('fa-caret-right');
      } else {
        el.removeClass('fa-caret-right').addClass('fa-caret-down');
      }
      return false;
  });
});
