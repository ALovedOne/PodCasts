var com = com || {}
com.frz = com.frz || {}
com.frz.podcast = {}
com.frz.podcast.vars = {}

com.frz.podcast.get_item = function(div, item_name) {
  return $(div).parents("." + item_name);
}

com.frz.podcast.item_id = function(div, item_name) {
  item = com.frz.podcast.get_item(div, item_name);
  return item[0].getAttribute(item_name + "_id");
}

com.frz.podcast.play = function(evnt) {
  var args = {};
  args['show_id'] = com.frz.podcast.item_id(evnt.target,'show');

  Dajaxice.PodCasts.loadInstance(function(data) {
    var audio = $("#audio-element")[0];
    audio.src = data['url'];
    audio.startTime = 60;
    com.frz.podcast.vars.inst_id = data['inst_id'];

    audio.addEventListener('canplaythrough', function() {
      audio.currentTime = data['position'];
      audio.play();
      com.frz.podcast.vars.interval = setInterval(com.frz.podcast.podcast_update, 1000*60*2);
    });
    audio.addEventListener('pause', com.frz.podcast.podcast_update);
  }, args);
}

com.frz.podcast.podcast_update = function() {
  var audio = $("#audio-element")[0];
  var args = {};

  if (audio.paused) {
    clearInterval(com.frz.podcast.vars.interval);
    com.frz.podcast.vars.interval = 0;
  }

  args['inst_id'] = com.frz.podcast.vars.inst_id;
  args['curr_pos'] = audio.currentTime;

  Dajaxice.PodCasts.updateInstance(function(data) {
    } ,args);
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
  elements = $(".play-show");
  for (i = 0; i < elements.length; i++) {
    elements[i].onclick = com.frz.podcast.play;
  }
})
