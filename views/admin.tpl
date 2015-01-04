% setdefault('error', '')
% include('header.tpl')
% include('navbar.tpl')
<div id="contents">
	<div>
		<h1>Добавить админа</h1>
		<p>
			Введите email Google
		</p>
		<form action="/admin" method="post" class="message">
			<input type="text" name="mail" placeholder="email"></input>	
            <input type="submit" value="Добавить"/>
			<h4 style="color:#ff0000">{{error}}</h4>
		</form>
	</div>
	
	<h1>Список админов:</h1>
	% for admin in admins:
	<div class="posts">
    <h2>{{admin.admin_nick}}</h2> 
	<h3>Добавлен {{admin.date.strftime("%d.%m.%y  %H:%M")}} {{admin.ref_nick}}</h3>
    </div>
    % end
	
</div>

% include('footer.tpl')