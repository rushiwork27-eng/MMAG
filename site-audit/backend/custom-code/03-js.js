//You can replace offset value from here
var offset = 300
$(window).on('load scroll', function(){
	
	if( $(window).scrollTop() > offset ){
        $('body').addClass('show')
	}else{
        $('body').removeClass('show')
	}
})