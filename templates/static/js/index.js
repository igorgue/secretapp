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
       }
     });
    
    return false;
}


$(document).ready(function(){
    $('.clickAction').submit(function(){ return $(this).clickAction(); });
});