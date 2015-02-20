<script src="//vk.com/js/api/openapi.js" type="text/javascript"></script>

<div id="login_button" onclick="VK.Auth.login(authInfo);"></div>

<script language="javascript">
VK.init({
  apiId: {{id}}
});
function authInfo(response) {
  if (response.session) {
    alert('user: '+response.session.mid);
  } else {
    alert('not auth');
  }
}
VK.Auth.getLoginStatus(authInfo);
VK.UI.button('login_button');
</script>