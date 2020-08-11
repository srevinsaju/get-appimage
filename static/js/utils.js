/*
MIT License

Copyright (c) 2020
Srevin Saju <srevinsaju (at) sugarlabs (dot) org>
Manish <sugar (at) radii (dot) dev>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
function setCookie(cname, cvalue, exdays) {
  // A function to set cookie from document.cookie
  // https://www.w3schools.com/js/js_cookies.asp
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  const expires = 'expires='+ d.toUTCString();
  document.cookie = cname + '=' + cvalue + ';' + expires + ';path=/';
}

function getCookie(cname) {
  // A function to get cookie from document.cookie
  // https://www.w3schools.com/js/js_cookies.asp
  const name = cname + '=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}


function checkCookiesEnabledShowConsent() {
  /* Check if cookie consent has been accepted,
      if not, request the user for a consent
  */
  if (getCookie('saas-fun') == '' && getCookie('saas-cookie-consent-accepted') == ''
  ) {
    console.log('Cookie consent has not been accepted');
    // means cookie is not set yet!

    // add onclick event listener to setCookie cookie accepted
    $('#cookie-consent-accept-btn').click(function(evt) {
      setCookie('saas-cookie-consent-accepted', 'true', 30);
    });

    // ask the user for permission
    $('#cookieModal').modal('show');
    return false;
  } else {
    console.log('Cookie consent has already been accepted.');
    return true;
  }
}
