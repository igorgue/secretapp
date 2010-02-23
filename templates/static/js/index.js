$.prototype.clickAction = function(){
    /*
        Any "form" which is given the class "clickAction"
        which when submited will send its form contents to
        the url.
        
        The result shall be posted in the DOM element
        labeled with the class "filler".
        
        Then any elements marked with "hider" will be hidden (such as the button).
        
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


$(document).ready(function(){
    $('.clickAction').submit(function(){ return $(this).clickAction(); });
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


