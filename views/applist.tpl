% include('header.tpl')
% include('navbar.tpl')

	
<div id="contents">
	% for appl in appls:
	<div class="posts">
    <h2>{{appl.title}}</h2>   	
	<h3>{{appl.username}}</h3>
    <p>{{appl.content}}</p>
    <b>{{appl.date.strftime("%d.%m.%y  %H:%M")}}</b>
		
    </div>
    % end
</div>
		
% include('footer.tpl')

