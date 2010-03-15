$.prototype.clickAction = function(){
    /*
        Any "form" which is given the class "clickAction"
        will be turned into an ajax form.
        
        The result shall be posted in the DOM element
        labeled with the class "filler" (html injected).
        
        Then any elements marked with "hider" will be hidden (such as submit button).
        
        <form method="POST" action="/ajax/" class="clickAction">
            <div class="filler">3</div>
            <div class="hider"><input type="submit" /></div>
        </form>
    */
    var self = $(this);
    $.ajax({
       type: self.attr('method'),
       url: self.attr('action'),
       data: self.serialize(),
       success: function(msg){
           self.find('.filler').html(msg);
           self.find('.hider').hide();
           return false;
       },
       error: function(){
           return true;
       }
     });
     return false;
}

$.prototype.defaultText = function(text){
    /*
    Description:
        Applies default text to a input field.
        1. If empty onBlur place text.
        2. If text onFocus empties.
        3. If empty onLoad place text.
    Usage:
        $('#id_location').defaultText('Where are you looking?');
    */
    var self = $(this);
    self.blur(function(){
        if (self.val() === ''){
            self.val(text);
        }
    }).focus(function(){
        if (self.val() === text){
            self.val('');
        }
    });
    self.blur();
}

$.prototype.modalize = function() {
	/* 
	Description:
		Returns the contents of a link in a modal dialog box. Uses href attribute for the URL, and title
		attribute for the title of the modal dialog.
	Usage:
		<a href="/do/this/action/123/" class="modalize" title="Thanks for doing this">Do this</a>
	*/	
	var self = $(this);
    $.get(self.attr('href'), 
    	function(data) {
	  		self.after("<div id='modalized'>"+data+"</div>");
	  		$('#modalized').dialog({ title:self.attr('title'),modal:true,resizable:false,draggable:false, buttons: { "Close": function() { $(this).dialog("close"); } } });
		}
	);
    return false;
}

function swap(a, b) { $(a).hide(); $(b).show(); return false; }

/*

highlight v3

Highlights arbitrary terms.

<http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html>

MIT license.

Johann Burkard
<http://johannburkard.de>
<mailto:jb@eaio.com>

*/

jQuery.fn.highlight = function(pat) {
 function innerHighlight(node, pat) {
  var skip = 0;
  if (node.nodeType == 3) {
   var pos = node.data.toUpperCase().indexOf(pat);
   if (pos >= 0) {
    var spannode = document.createElement('span');
    spannode.className = 'highlight';
    var middlebit = node.splitText(pos);
    var endbit = middlebit.splitText(pat.length);
    var middleclone = middlebit.cloneNode(true);
    spannode.appendChild(middleclone);
    middlebit.parentNode.replaceChild(spannode, middlebit);
    skip = 1;
   }
  }
  else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
   for (var i = 0; i < node.childNodes.length; ++i) {
    i += innerHighlight(node.childNodes[i], pat);
   }
  }
  return skip;
 }
 return this.each(function() {
  innerHighlight(this, pat.toUpperCase());
 });
};

jQuery.fn.removeHighlight = function() {
 return this.find("span.highlight").each(function() {
  this.parentNode.firstChild.nodeName;
  with (this.parentNode) {
   replaceChild(this.firstChild, this);
   normalize();
  }
 }).end();
};


$(document).ready(function(){    
    // actions which handle the "rewritten logic"
    $('.clickAction').submit(function(){ return $(this).clickAction(); });
    $('a.modalize').click( function() { return $(this).modalize();} )
	$('.rewritten').click(function() {
		$(this).parents('.moderation_holder').children(':first').show();
		return false;
	});
	$('.close_explaination').click(function(){
		$(this).parent().hide();
		return false;
	});
	$('#top_query').defaultText('Search');
});

/**
 * Fill text box with prompt text in sensible way
 */
var configTextBoxPrompt = function(id, message) {
	var a = $(id);
	if (!a) return;
	if (!a.val()) {
		a.val(message);
		a.focus(function(b, ev2) {
			if (a.val() == message) a.val('');
		});
		a.blur(function(b, ev2) {
			if (a.val() == '') a.val(message);
		});
	}
}


