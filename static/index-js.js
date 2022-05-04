// 로그아웃은 내가 가지고 있는 토큰만 쿠키에서 없애면 됩니다.
  function logout(){
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href='/login'
  }