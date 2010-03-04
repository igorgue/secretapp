// publish to facebook function

function publish_to_facebook(user_message, attachment){
	var umessage = user_message
	var attachm = attachment
	// checking permissions
	FB.Facebook.apiClient.users_hasAppPermission("publish_stream",
		function(result, exception){
			if (result == 0){
				// permissions have not yet been granted
				FB.Connect.showPermissionDialog("publish_stream", function(perms){
				// check if permission has been granted now
				if (perms === 'publish_stream'){
					// permission granted
					FB.Connect.streamPublish(umessage, attachm, null, null, null, fbcallback, true, null)
					} else {
					// permission not granted, ask if user want to post
					FB.Connect.streamPublish(umessage, attachm, null, null, null, fbcallback, false, null)
					}
				});
				} else{
				// permanent permission to publish, autopost
				FB.Connect.streamPublish(umessage, attachm, null, null, null, fbcallback, true, null)
				}
				});
}

// ajax function to submit comments, and to also publish on facebook if desired
$(document).ready(function(){
	$('.commentsubmit').click(function(){
		$(this).attr("disabled", "true");
		var category = $(this).attr('category')
		var art = $(this).attr('art')
		var comment = $('#'+$(this).attr('category')).val()
		var lang = $(this).attr('lc')
		var destination = $(this).attr('destination')
		$.post('/'+lang+'/artcomment/', {
			comment: comment,
			category: category,
			art: art,
			lang: lang
		},
		function(data) {
			new_comment = data.new_html
			$('.all'+destination).append(new_comment);
			$('#comment'+data.commentid).fadeIn('slow');
			$('#'+category).val('');
			$('.commentsubmit').removeAttr('disabled')
		// check if user wants to also publish on facebook
		fbpost = $('#fbpublish').attr('checked')
		if (fbpost == true){
			caption = $('#infodiv').attr('image_caption');
			this_url = window.location.href;
			thumb = 'http://'+ window.location.host + $('#infodiv').attr('fbthumb');
			user_message = 'commented on friends-of-art.net'
			attachment = {
			'name': caption, 
			'href': this_url,
			'caption': '',
			'description': data.comment,
			'media': [{ 'type': 'image', 'src': thumb, 'href': this_url}]
				};
			publish_to_facebook(user_message, attachment)
		} else {
			void(0)
		}
		}, "json");
	});
});