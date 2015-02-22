<script src="//vk.com/js/api/openapi.js" type="text/javascript"></script>
<script type="text/javascript">
  VK.init({
    apiId: {{id}}
  });

function CheckLogin(response) {
  if (response.session) {
    window.location.href = "/vklogindo"
  } else {
    VK.Auth.Login(CheckLoginTry)
  }
}

function CheckLoginTry(response) {
  if (response.session) {
    window.location.href = "/vklogindo"
  } else {
    window.location.href = "/"
  }
}

VK.Auth.getLoginStatus(CheckLogin);
</script>
