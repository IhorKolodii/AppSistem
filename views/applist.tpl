% include('header.tpl')
% include('navbar.tpl')

	
<div id="contents">
	% for appl in appls:
	<div>
    <h2>{{appl.title}}</h2>
    <p>{{appl.content}}</p>
    <b>{{appl.date}}</b>
    </div>
    % end
</div>
		
% include('footer.tpl')