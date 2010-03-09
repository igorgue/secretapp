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
	})
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


