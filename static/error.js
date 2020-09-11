const previouslocation = document.querySelector('.previouslocation_btn');

// previouslocation.setAttribute('href', document.referrer);

// We can't let the browser use the above href for navigation. If it does, 
// the browser will think that it is a regular link, and place the current 
// page on the browser history, so that if the user clicks "back" again,
// it'll actually return to this page. We need to perform a native back to
// integrate properly into the browser's history behavior
previouslocation.onclick = function() {
  history.back();
  return false;
};