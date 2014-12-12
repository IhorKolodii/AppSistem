% include('header.tpl')
% include('navbar.tpl')
<div id="contents">
	<div class="section">
		<h1>Заявка</h1>
		<p>
			Пожалуйста заполните все поля.
		</p>
		<form action="/add" method="post" class="message">
			<input type="text" name="title" placeholder="Заголовок"></input>				
			<textarea name="content" placeholder="Текст заявки" rows="16"></textarea>
			<input type="submit" value="Послать"/>
		</form>
	</div>
	
	<div class="section contact">
		<p>
			При необходимости свяжитесь с нами по телефону <span>877-433-8137</span>
		</p>
		<p>
			Заходите на сайт фестиваля: <span>Ханифест<br> Лучший Харьковский Аниме Фестиваль</span>
		</p>
	</div>
</div>

% include('footer.tpl')