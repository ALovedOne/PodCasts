var com = com || {}
com.frz = com.frz || {}
com.frz.podcast = {}

com.frz.podcast.get_item = function(div, item_name) {
  return $(div).parents("." + item_name);
}

com.frz.podcast.item_id = function(div, item_name) {
  item = com.frz.podcast.get_item(div, item_name);
  return item[0].getAttribute(item_name + "_id");
}

com.frz.podcast.play_url = function(url) {
  if(url == "") {
    return;
  }
  audio = $("#audio-element")[0];
  audio.src = url;
  
  Dajaxice.PodCasts.loadInstance(PodCasts_play_url_cb, data);

  audio.play();
  setInterval(podcast_update, 60*1000);
}

com.frz.podcast.podcast_pause = function() {

}

com.frz.podcast.podcast_update = function() {

}

com.frz.podcast.update_favorite = function(evnt){
  var args = {};
  args['PodCast_id']=com.frz.podcast.item_id(evnt.target,'podcast');
  Dajaxice.PodCasts.toggleFavorite(function(data) {
    var item = com.frz.podcast.get_item(evnt.target, 'podcast');
    item.removeClass('favorite');
    if(data['needs_auth']) {
      window.location = '/login';
    } else if(data['favorite']) {
      item.addClass('favorite');
    }
  }, args);
}

$(document).ready(function() {
  elements = $(".fav-img");
  for (i = 0; i < elements.length; i++) {
    elements[i].onclick = favorite_podcast;
  }
  elements = $(".update_favorite");
  for (i = 0; i < elements.length; i++) {
    elements[i].onclick = com.frz.podcast.update_favorite;
  }
})
