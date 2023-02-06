

$(document).ready(function(){
	
	$(document).on('click', '.button', function(event){
		var ind = this.id
		var url = this.name
		var press = this.value
		var title = this.title


		$('#'+ind).addClass('writen')
				
		// if(clicked != 'avoid'){
		// $(this).siblings('tr').removeClass('onclick')
		// $(this).addClass('onclick')
		$.ajax({
			data:{
				ind : ind,
				url: url,
				press : press,
				title : title,
				cmd : "readall"
			},
			type : 'POST',
			url : '/donga/dangbun/naver/write'
		})
		.done(function(data){


			var brRegex = /<br\s*[\/]?>/gi;
			var textArea = document.createElement('textArea');
			textArea.value = data.replace(brRegex, "\r\n");
			document.body.appendChild(textArea);
			textArea.select();
			document.execCommand('copy');
			document.body.removeChild(textArea);
			alert(data+"\n\n\n클립보드에 복사됐습니다");
			// console.log(data)
			// $('#content').html(data)
		})
		//아직 on click
		// event.preventDefault();

		;	
		});
});
