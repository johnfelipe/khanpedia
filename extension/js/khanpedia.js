// Bad code ahead, ye be warned
$.getJSON(chrome.extension.getURL("khantent.json"), function(khantent) {
  var title = $("#firstHeading").text().split(" (")[0].toLowerCase(); 
  var match = khantent[title]; 
  if (match) {
    page_link = '<a id="page_link" href="http://khanacademy.org/search?page_search_query=' + title.replace(" ", "+") + '">View on Khan Academy</a>'; 
    $("#firstHeading").after(page_link); 
  }
  var poppedup;
  $("#mw-content-text a").each(function(index) {
    title = $(this).attr("title"); 
    if (title) {
      title = title.split(" (")[0].toLowerCase(); 
      match = khantent[title]; 
      if (match) {
        var content = '<a href="{{khan_link}}"><img id="khan_img" src="{{khan_img}}"/></a><a href="{{wiki_link}}"><img id="wiki_img" src="{{wiki_img}}" /></a>'; 
        var data = {
          "khan_img": chrome.extension.getURL("img/khan.png"), 
          "khan_link": "http://khanacademy.org/search?page_search_query=" + title.replace(" ", "+"), 
          "wiki_img": chrome.extension.getURL("img/wiki.png"), 
          "wiki_link": $(this).attr("href")
        }
        var template = Handlebars.compile(content); 
        // Credit: Emily for legit JS
        $(this)
          .addClass("khantent")
          .click(function() {
            if (poppedup != null) {
              $(poppedup).popover('hide');
            }
            $(this).popover('toggle'); 
            poppedup = this;
            return false; 
          })
          .popover({
            "placement": "top", 
            "trigger": "manual", 
            "content": template(data)
          });
        var that = this;
        $("body").click(function() { poppedup = null; $(that).popover('hide'); }); 
      }
    }
  }); 
}); 
