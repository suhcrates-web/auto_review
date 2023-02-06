

$(document).ready(function(){
	
	$(document).on('click', '#make_box', function(event){
		var state = this.getAttribute("state");
		
		// alert('shit')
		// var clicked = this.id
		// if(clicked != 'avoid'){
		// $(this).siblings('tr').removeClass('onclick')
		// $(this).addClass('onclick')
		$('#make_box').html("작성중....(10초 소요됨)")
		$.ajax({
			data:{
				cmd : "giveme",
				version : "1",
				state: state
			},
			type : 'POST',
			url : '/make_review'
		})
		.done(function(data){
			if (data['cmd'] =='not_yet'){
				$('#make_box').html("작성버튼")
				location.reload()
				alert(data.message)}
			else if (data['cmd'] =='ok'){
				$('#content_box').html(data.message)
				$('#now').html(data.time)
				$('#make_box').html("작성완료~~")
				
			}
		});

		
	});

	$(document).on('click', '#copy', function(){

		var copy0 = $('#content_box') //.text();	
		var brRegex = /<br\s*[\/]?>/gi;
		var textArea = document.createElement('textArea');
		textArea.value = copy0.html().replace(brRegex, "\r\n");
		document.body.appendChild(textArea);
		textArea.select();
		document.execCommand('copy');
		document.body.removeChild(textArea);
		alert("클립보드에 복사됐습니다");
			
	});
});
